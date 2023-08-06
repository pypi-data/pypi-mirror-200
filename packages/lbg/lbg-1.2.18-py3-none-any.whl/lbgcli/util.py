import base64
import os
import ssl
import sys
import urllib.request
import zipfile

import requests
from tqdm import tqdm
from urllib.parse import urlparse

ssl._create_default_https_context = ssl._create_unverified_context


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').n")


def zip_dir(zip_path, out_file, save_files=None):
    if save_files is None:
        save_files = []
    dic_to_save = {}
    for tmp_file in save_files:
        dic_to_save[tmp_file] = 1
    zip_file = zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(zip_path):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(zip_path, '')
        for filename in filenames:
            # 获取相对路径
            file_path = os.path.join(fpath, filename)
            if dic_to_save and (file_path not in dic_to_save):
                continue
            else:
                try:
                    os.stat(os.path.join(path, filename))
                    zip_file.write(os.path.join(path, filename),
                                   os.path.join(fpath, filename))
                except FileNotFoundError:
                    continue
    zip_file.close()


def unzip_file(zip_file_path, out_path):
    zip_file = zipfile.ZipFile(zip_file_path, "r", zipfile.ZIP_DEFLATED)
    for tmp_file in zip_file.namelist():
        zip_file.extract(tmp_file, out_path)


class UrlRetrieveTqdm(tqdm):
    last_block = 0

    def update_to(self, block_num=1, block_size=1, total_size=None):
        if total_size is not None:
            self.total = total_size
        self.update((block_num - self.last_block) * block_size)
        self.last_block = block_num
        self.set_description(
            f"{round(block_num * block_size / 1024 / 1024, 2)}/{round(total_size / 1024 / 1024, 2)} Mb")


def download(url, target, suffix='.zip'):
    retry = 3
    for r in range(retry):
        try:
            with UrlRetrieveTqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, leave=False) as t:
                urllib.request.urlretrieve(url, str(target) + suffix, reporthook=t.update_to)
            break
        except Exception as e:
            if r < 2:
                print(f'Download Failed. Attempt # {r + 1}')
                print(e)
            else:
                print('Error encountered at third attempt')
                print(e)
                return False
    unzip_file(str(target) + suffix, target)
    os.remove(str(target) + suffix)
    return True


def base64url_decode(s) -> bytes:
    if isinstance(s, str):
        s = s.encode("ascii")

    rem = len(s) % 4

    if rem > 0:
        s += b"=" * (4 - rem)

    return base64.urlsafe_b64decode(s)


def is_bohr_instance():
    retry = 5
    is_bohr = False
    TEST_ACCOUNT_ID = '1836303934781095'
    PROD_ACCOUNT_ID = '1761286239356625'
    for i in range(retry):
        try:
            resp = requests.get("http://100.100.100.200/latest/meta-data/owner-account-id", timeout=1)
            resp.raise_for_status()
            if resp.ok:
                if resp.text.strip() == TEST_ACCOUNT_ID or resp.text == PROD_ACCOUNT_ID:
                    is_bohr = True
                    break
            is_bohr = False
            break
        except:
            is_bohr = False
    return is_bohr
