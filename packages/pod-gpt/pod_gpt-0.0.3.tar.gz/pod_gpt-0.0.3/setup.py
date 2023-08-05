# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pod_gpt']

package_data = \
{'': ['*']}

install_requires = \
['langchain>=0.0.125,<0.0.126',
 'pytube>=12.1.3,<13.0.0',
 'torch>=2.0.0,<3.0.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'pod-gpt',
    'version': '0.0.3',
    'description': 'Package for building podcast search indexes.',
    'long_description': '# PodGPT',
    'author': 'James Briggs',
    'author_email': 'james@aurelio.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
