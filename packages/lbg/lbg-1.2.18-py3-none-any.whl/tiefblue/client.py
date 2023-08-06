import asyncio
import base64
import json
import os.path
import shutil
from concurrent.futures import ThreadPoolExecutor

import oss2
from tqdm import tqdm
import requests

_DEFAULT_CHUNK_SIZE = 50 * 1024 * 1024
_DEFAULT_ITERATE_MAX_OBJECTS = 50


class Parameter(object):
    contentType: str
    contentEncoding: str
    contentLanguage: str
    contentDisposition: str
    cacheControl: str
    acl: str
    expires: str
    userMeta: dict
    predefinedMeta: str


class TiefblueException(Exception):
    code: int
    title: str
    msg: str
    reference: str

    def __str__(self):
        return f'code: {self.code},title: {self.title},msg: {self.msg},reference: {self.reference}'


class Client:
    TIEFBLUE_HEADER_KEY = 'X-Storage-Param'

    def __init__(self, base_url: str, token=''):
        self._base_url = base_url.rstrip('/')
        self._header = {}
        self._token = token

    def write(self, object_key: str, body, parameter=None, progress_bar=None):
        param = {
            "path": object_key,
        }
        if parameter:
            param["option"] = parameter.__dict__

        session = self._session(header_param=param)
        req = session.post(f"{self._base_url}/api/upload/binary", data=body)
        self._raise_error(req)
        return req.json()

    def read(self, object_key: str, ranges: str, writer, parameter=None):
        session = self._session()
        if ranges != "":
            session.headers['Range'] = ranges
        with session.get(f"{self._base_url}/api/download/{object_key}", stream=True) as req:
            self._raise_error(req, content_json=False)
            shutil.copyfileobj(req.raw, writer)
        return

    def meta(self, object_key: str):
        session = self._session()
        req = session.get(f"{self._base_url}/api/meta/{object_key}")
        self._raise_error(req)
        return req.json().get('data')

    def delete(self, object_key: str):
        session = self._session()
        req = session.delete(f"{self._base_url}/api/delete/{object_key}")
        self._raise_error(req)
        return req.json().get('data')

    def exist(self, object_key: str):
        req = self.meta(object_key)
        return req.get('exist', False)

    def iterate(self, prefix: str, next_token='', max_objects=50):
        session = self._session()
        req = session.get(f"{self._base_url}/api/iterate/{prefix}", params={
            "nextToken": next_token,
            "maxObjects": max_objects
        })
        self._raise_error(req)
        return req.json().get('data')

    def _dump_parameter(self, parameter):
        j = json.dumps(parameter)
        return base64.b64encode(j.encode()).decode()

    def _session(self, header_param: dict = None):
        header = {}
        if self._token:
            header['Authorization'] = f'Bearer {self._token}'
        if header_param is not None:
            header[self.TIEFBLUE_HEADER_KEY] = self._dump_parameter(header_param)
        session = requests.session()
        session.headers = header
        return session

    def _raise_error(self, req, content_json: bool = True):
        if content_json:
            data = req.json()
            if 'error' in data:
                exep = TiefblueException()
                exep.code = data.get('code')
                err = data.get('error', {})
                exep.title = err.get('title')
                exep.msg = err.get('msg')
                exep.reference = err.get('reference')
                raise exep
        req.raise_for_status()

    def init_upload_by_part(self, object_key: str, parameter=None):
        body = {
            'path': object_key
        }
        if parameter is not None:
            body['option'] = parameter.__dict__
        session = self._session()
        resp = session.post(f"{self._base_url}/api/upload/multipart/init", json=body)
        self._raise_error(resp)
        return resp.json().get('data')

    def upload_by_part(self, object_key: str, initial_key: str, chunk_size: int, number: int, body):
        param = {
            'initialKey': initial_key,
            'number': number,
            'partSize': chunk_size,
            'objectKey': object_key
        }
        session = self._session(header_param=param)
        resp = session.post(f"{self._base_url}/api/upload/multipart/upload", data=body)
        self._raise_error(resp)
        return resp.json().get('data')

    def complete_upload_by_part(self, object_key, initial_key, part_string):
        body = {
            'path': object_key,
            'initialKey': initial_key,
            'partString': part_string
        }
        session = self._session()
        resp = session.post(f"{self._base_url}/api/upload/multipart/complete", json=body)
        self._raise_error(resp)
        return resp.json().get('data')

    def upload_from_file(self, object_key: str, file_path: str, chunk_size: int = _DEFAULT_CHUNK_SIZE, parameter=None,
                         progress_bar=False, need_parse=False):
        if not os.path.exists(file_path):
            raise FileNotFoundError
        if os.path.isdir(file_path):
            raise IsADirectoryError
        if need_parse:
            _, _, object_key = self._parse_app_name_and_tag(object_key)
        size = os.path.getsize(file_path)
        _, disposition = os.path.split(file_path)
        if parameter is None:
            parameter = Parameter()
        parameter.contentDisposition = f'attachment; filename="{disposition}"'
        bar_format = "{l_bar}{bar}| {n:.02f}/{total:.02f} %  [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        with open(file_path, 'r') as f:
            pbar = tqdm(total=100, desc=f"Uploading {disposition}", smoothing=0.01, bar_format=bar_format,
                        disable=not progress_bar)
            f.seek(0)
            if size < _DEFAULT_CHUNK_SIZE * 2:
                self.write(object_key, f.buffer, parameter)
                pbar.update(100)
                pbar.close()
                return
            chunks = split_size_by_part_size(size, chunk_size)
            initial_key = self.init_upload_by_part(object_key, parameter).get('initialKey')
            part_string = []
            for c in chunks:
                f.seek(c.Offset)
                num_to_upload = min(chunk_size, size - c.Offset)
                part_string.append(self.upload_by_part(object_key, initial_key, chunk_size=c.Size, number=c.Number,
                                                       body=f.buffer.read(c.Size)).get('partString'))
                percent = num_to_upload * 100 / (size + 1)
                pbar.update(percent)
            pbar.close()
            return self.complete_upload_by_part(object_key, initial_key, part_string)

    def download_from_file(self, object_key, file_path):
        session = self._session()
        with session.get(f"{self._base_url}/api/download/{object_key}", stream=True) as req:
            try:
                self._raise_error(req, content_json=False)
            except requests.exceptions.HTTPError as e:
                if req.status_code == 401:
                    self._raise_error(req, content_json=True)
                raise e
            with open(file_path, 'w') as f:
                shutil.copyfileobj(req.raw, f.buffer)

    def _parse_app_name_and_tag(self, input_path: str):
        l = input_path.split('/')
        if len(l) < 3:
            return "", "", l
        return l[0], l[1], "/".join(l[2:])

    def list(self, prefix: str = '', next_token: str = '', recursive: bool = False,
             max_objects=_DEFAULT_ITERATE_MAX_OBJECTS):
        session = self._session()
        if max_objects <= 0:
            max_objects = _DEFAULT_ITERATE_MAX_OBJECTS
        data = {
            'prefix': prefix,
            'maxObjects': max_objects
        }
        if recursive:
            data['recursive'] = True
        if next_token != '':
            data['nextToken'] = next_token
        req = session.post(f"{self._base_url}/api/iterate", json=data)
        self._raise_error(req)
        return req.json().get('data')

    def copy(self, src: str, dst: str):
        session = self._session()
        data = {
            'sourcePath': src,
            'destinationPath': dst
        }
        req = session.post(f"{self._base_url}/api/copy", json=data)
        self._raise_error(req)
        return req.json().get('data')


class Chunk:
    Number: int
    Offset: int
    Size: int


def split_size_by_part_size(total_size: int, chunk_size: int):
    if chunk_size < _DEFAULT_CHUNK_SIZE:
        chunk_size = _DEFAULT_CHUNK_SIZE
    chunk_number = int(total_size / chunk_size)
    if chunk_number >= 10000:
        raise TooManyChunk
    chunks = []
    for i in range(chunk_number):
        c = Chunk()
        c.Number = i + 1
        c.Offset = i * chunk_size
        c.Size = chunk_size
        chunks.append(c)

    if total_size % chunk_size > 0:
        c = Chunk()
        c.Number = len(chunks) + 1
        c.Offset = len(chunks) * chunk_size
        c.Size = total_size % chunk_size
        chunks.append(c)
    return chunks


def partial_with_start_from(start_bytes):
    return f'bytes={start_bytes}-'


def partial_with_end_from(end_bytes):
    return f'bytes=-{end_bytes}'


def partial_with_range(start_bytes, end_bytes):
    return f'bytes={start_bytes}-{end_bytes}'


TooManyChunk = Exception("too many chunks, please consider increase your chunk size")
