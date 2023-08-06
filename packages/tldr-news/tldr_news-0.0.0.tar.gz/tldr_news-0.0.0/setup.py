# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tldr_news']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'requests>=2.28.2,<3.0.0',
 'textual>=0.15.1,<0.16.0']

entry_points = \
{'console_scripts': ['tldr_news = tldr_news.cli:cli']}

setup_kwargs = {
    'name': 'tldr-news',
    'version': '0.0.0',
    'description': '',
    'long_description': '## TLDR News Terminal\n\nThis is a simple terminal application that shows the latest tech news headlines from the [TLDR Newsletter](https://tldr.tech/).\n\nThe application is written in Python, uses the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library to parse the HTML content of the newsletter and uses [Textual](textual.textualize.io/) library to render the content in the terminal.\n\n![Preview App](images/preview-app.png)\n\n### <b>Usage</b>\n\n```bash\npip install tldr_news\n```\n\n### <b>Installation</b>\n\nTo install the application, simply run the following command after cloning the repository:\n\n1. Install dependencies\n\n```bash\npoetry install && poetry shell\n```\n\n2. Run the application\n\n```bash\npoetry run tldr_news\n```\n\n### <b>DISCLAIMER</b>\n\nThis is not an official TLDR Newsletter product, but a personal project coming from my love with this newsletter. I am not affiliated with TLDR Newsletter in any way.\n\nAll the newsletter content is owned by TLDR Newsletter and I am not responsible for any of the content.\n',
    'author': 'Harry Tran',
    'author_email': 'huytran.quang080199@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
