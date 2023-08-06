# 项目描述

一个用于加密str型和bytes型数据的加密器。

1、底层加密算法为AES-CBC-256。

2、加密时，会自动创建随机salt、随机iv、原始明文的校验值，并把校验值添加到密文中。

3、解密时，会自动根据校验值校验“解密得到的明文”与“原始明文”是否一致。

# 安装与文档

安装：`pip install encrypt256`

[文档](https://github.com/lcctoor/lccpy/blob/main/encrypt256/docs/doc.md)

# Bug提交、功能提议

您可以通过 [Github-Issues](https://github.com/lcctoor/lccpy/issues)、[微信](https://raw.githubusercontent.com/lcctoor/me/main/author/WeChatQR.jpg)、[技术交流群](https://raw.githubusercontent.com/lcctoor/me/main/ExchangeGroup/PythonTecQR.jpg) 与我联系。

# 关于作者

作者：许灿标

邮箱：lcctoor@outlook.com

[主页](https://github.com/lcctoor/me/blob/main/home.md) | [微信](https://raw.githubusercontent.com/lcctoor/me/main/author/WeChatQR.jpg) | [Python技术微信交流群](https://raw.githubusercontent.com/lcctoor/me/main/ExchangeGroup/PythonTecQR.jpg)

开源项目：[让 Python 更简单一点](https://github.com/lcctoor/lccpy#readme)

# 语法预览

导入：

```python
from encrypt256 import Encrypt256
```

创建加密器：

```python
password1 = 123456789  # 支持int型密钥
password2 = '黄河之水天上来'  # 支持str型密钥
password3 = '床前明月光'.encode('utf8')  # 支持bytes型密钥

enctool = Encrypt256(password1)  # 创建加密器
```

加密：

```python
# 加密str型数据
p1 = '人生自古谁五死'
c1 = enctool.encrypt(p1, checkSize=32)

# 加密bytes型数据
p2 = '莎士比亚'.encode('utf8')
c2 = enctool.encrypt(p2, checkSize=64)
```

解密：

```python
p11 = enctool.decrypt(c1)
p22 = enctool.decrypt(c2)

assert p1 == p11
assert p2 == p22

assert type(p1) is type(p11)
assert type(p2) is type(p22)
```
