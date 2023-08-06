# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_chatppt']

package_data = \
{'': ['*']}

install_requires = \
['icrawler>=0.6.6,<0.7.0',
 'nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot2>=2.0.0rc3,<3.0.0',
 'openai>=0.27.1,<0.28.0',
 'python-pptx>=0.6.21,<0.7.0']

setup_kwargs = {
    'name': 'nonebot-plugin-chatppt',
    'version': '0.0.1',
    'description': 'A nonebot plugin for generating PPT slides from ChatGPT',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-chatppt\n</div>\n\n## 介绍\n- 本插件基于OpenAI的API开发，在nonebot框架下实现一个AI生成指定主题PPT的文件并上传到群文件中。\n\n![](demo.png)\n## 安装\n\n* 手动安装\n  ```\n  git clone https://github.com/Alpaca4610/nonebot-plugin-chatppt.git\n  ```\n\n  下载完成后在bot项目的pyproject.toml文件手动添加插件：\n\n  ```\n  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot-plugin-chatppt"]\n  ```\n* 使用 pip\n  ```\n  pip install nonebot-plugin-chatppt\n  ```\n\n## 配置文件\n\n在Bot根目录下的.env文件中追加如下内容：\n\n```\nOPENAI_API_KEY = key\n```\n\n可选内容：\n```\nOPENAI_HTTP_PROXY = "http://127.0.0.1:8001"    # 中国大陆/香港IP调用API请使用代理访问api,否则有几率会被封禁\nOPENAI_MODEL_NAME = "xxxxx"   # 使用的模型名称\nSLIDES_LIMIT = "xxxxx"   # 生成PPT页数的上限，不设置默认为10\n```\n\n\n## 使用方法\n\n- 生成PPT\n```\nchatppt 主题：XXXX，页数：XXXXX\n```\n- 删除当前用户缓存文件\n```\n删除缓存PPT\n```\n- 删除所有用户缓存文件\n```\n删除所有缓存PPT\n```\n\n## Todo\n\n- [ ] 优化生成内容\n- [ ] 完善插入图片功能\n\n## 核心代码\n\n核心代码来源于：[Python-PPTX-ChatGPT-Presentation-Generator](https://github.com/AmNotAGoose/Python-PPTX-ChatGPT-Presentation-Generator)\n',
    'author': 'Alpaca',
    'author_email': 'alpaca@bupt.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
