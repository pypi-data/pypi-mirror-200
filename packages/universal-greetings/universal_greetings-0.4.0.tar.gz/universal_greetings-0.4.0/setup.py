# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['universalgreetings']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'urllib3>=1.26.12,<2.0.0']

setup_kwargs = {
    'name': 'universal-greetings',
    'version': '0.4.0',
    'description': 'Universal Greetings Library',
    'long_description': '# Universal Greetings Library for Python\n\nUniversal Greetings  description\n\n\n## Get started\n\n```bash\npoetry add universal-greetings\n```\n\n```python\nfrom universalgreetings import Hello\n\nhello=Hello()\n\nhello.sayHello()\n\n```\n',
    'author': 'Alan S. Ferreira',
    'author_email': 'alansferreira1984@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alelltech-backstage-demo/python-library-universal-greetings',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
