# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['uagents',
 'uagents.contrib',
 'uagents.contrib.protocols',
 'uagents.crypto',
 'uagents.storage']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'apispec>=6.0.2,<7.0.0',
 'bech32>=1.2.0,<2.0.0',
 'cosmpy>=0.6.0,<0.7.0',
 'ecdsa>=0.18.0,<0.19.0',
 'msgpack>=1.0.4,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'uvicorn>=0.19.0,<0.20.0',
 'websockets>=10.4,<11.0']

setup_kwargs = {
    'name': 'uagents',
    'version': '0.3.2',
    'description': 'Lightweight framework for rapid agent-based development',
    'long_description': 'The **μAgents** (micro-Agents) project is a fast and lightweight framework that makes it easy to build agents for all kinds of decentralised use cases.\n\n## Installation\n\nInstall μAgents for Python 3.8, 3.9, or 3.10:\n\n```bash\npoetry install\npoetry shell\n```\n\n## Documentation\n\nBuild and run the docs locally with:\n\n```bash\nmkdocs serve\n```\n\nOr go to the official docs site: https://docs.fetch.ai/uAgents.\n\n## Examples\n\nThe [`examples`](https://github.com/fetchai/uAgents/tree/main/examples) folder contains several examples of how to create and run various types of agents.\n\n## Contributing\n\nAll contributions are welcome! Remember, contribution includes not only code, but any help with docs or issues raised by other developers. See our [contribution guidelines](https://github.com/fetchai/uAgents/blob/main/CONTRIBUTING.md) for more details.\n\n### Development Guidelines\n\nRead our [development guidelines](https://github.com/fetchai/uAgents/blob/main/DEVELOPING.md) to learn some useful tips related to development.\n\n### Issues, Questions and Discussions\n\nWe use [GitHub Issues](https://github.com/fetchai/uAgents/issues) for tracking requests and bugs, and [GitHub Discussions](https://github.com/fetchai/uAgents/discussions) for general questions and discussion.\n\n## License\n\nThe μAgents project is licensed under [Apache License 2.0](https://github.com/fetchai/uAgents/blob/main/LICENSE).\n\n',
    'author': 'Ed FitzGerald',
    'author_email': 'edward.fitzgerald@fetch.ai',
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
