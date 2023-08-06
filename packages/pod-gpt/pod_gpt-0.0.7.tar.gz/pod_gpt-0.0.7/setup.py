# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pod_gpt', 'pod_gpt.models']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python>=0.2.0,<0.3.0',
 'langchain>=0.0.125,<0.0.126',
 'openai>=0.27.2,<0.28.0',
 'pinecone-client[grpc]>=2.2.1,<3.0.0',
 'pytube>=12.1.3,<13.0.0',
 'tiktoken>=0.3.3,<0.4.0',
 'torch>=2.0.0,<3.0.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'pod-gpt',
    'version': '0.0.7',
    'description': 'Package for building podcast search indexes.',
    'long_description': '# PodGPT\n\nInstall with:\n\n```\n!pip install pod-gpt\n```\n',
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
