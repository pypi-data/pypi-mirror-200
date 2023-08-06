# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiowechatpayv3']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=40.0.1,<41.0.0', 'httpx>=0.23.3,<0.24.0']

setup_kwargs = {
    'name': 'aiowechatpayv3',
    'version': '0.1.0',
    'description': '',
    'long_description': '# 微信支付 API v3 Python SDK\n\n[![PyPI version](https://badge.fury.io/py/wechatpayv3.svg)](https://badge.fury.io/py/wechatpayv3)\n[![Download count](https://img.shields.io/pypi/dm/wechatpayv3)](https://img.shields.io/pypi/dm/wechatpayv3)\n\n## 介绍\n异步版本微信支付包，fork自[wechatpayv3](https://github.com/minibear2021/wechatpayv3)\n微信支付接口 V3 版 python 库。\n\n文档完善中，暂时参考[微信支付 API v3 文档](https://wechatpay-api.gitbook.io/wechatpay-api-v3/)。\n',
    'author': 'yuxf',
    'author_email': 'yuxf@unitechs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
