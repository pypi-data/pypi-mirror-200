# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['quantuloop_aws_client']

package_data = \
{'': ['*']}

install_requires = \
['bcrypt>=4.0.1,<5.0.0',
 'cryptography>=40.0.1,<41.0.0',
 'ket-lang>=0.5.1,<0.6.0',
 'pyjwt>=2.6.0,<3.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'quantuloop-aws-client',
    'version': '2023.3b2',
    'description': '',
    'long_description': '# Quantuloop AWS Client\n\nClient to access your quantum simulator server on AWS. For more information, visit <https://simulator.quantuloop.com>.\n',
    'author': 'Quantuloop',
    'author_email': 'dev@quantuloop.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
