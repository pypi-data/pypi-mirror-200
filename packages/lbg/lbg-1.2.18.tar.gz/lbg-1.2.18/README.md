# 简介
Lebesgue-Utility提供了访问DP-Lebesgue的Python接口和Shell交互工具，可用于上传文件、提交任务、查询任务状态、获取任务结果、停止任务等。


# 下载与安装

Lebesgue-Utility支持Python3，尚未在Python2上进行测试。
当前Lebesgue-Utility提供pip方式安装
```shell
pip3 install git+https://git.dp.tech/lebesgue/lebesgue-utility
```
运行方式，在命令行中输入：
```shell
lbg
```

 # 发布

pypi上注册一个开发者账号
https://pypi.org/

管理员邀请到lbg项目下
开发者确认邀请
安装依赖
```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

```
进入代码目录，编译
```
python3 -m build
```
在pypi网站用户设置 add api token，复制到本地
```
vim ~/.pypirc

[pypi]
  username = __token__
  password = xxxx
```
上传到pypi
```
python3 -m twine upload dist/*
```