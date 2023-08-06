# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['babble', 'babble.crypto']

package_data = \
{'': ['*']}

install_requires = \
['bech32>=1.2.0,<2.0.0',
 'ecdsa>=0.18.0,<0.19.0',
 'eciespy>=0.3.13,<0.4.0',
 'pycryptodome>=3.16.0,<4.0.0',
 'pyjwt>=2.6.0,<3.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'fetchai-babble',
    'version': '0.1.1',
    'description': 'A simple python library for interacting with the Fetch.ai messaging service (called Memorandum)',
    'long_description': '# Babble\n\nA simple python library for interacting with the Fetch.ai messaging service (called Memorandum)\n\n## Quick Example\n\n```python\nfrom babble import Client, Identity\n\n# create a set of agents with random identities\nclient1 = Client(\'agent1.....\', Identity.generate())\nclient2 = Client(\'agent1.....\', Identity.generate())\n\n# send a message from one client to another\nclient1.send(client2.delegate_address, "why hello there")\n\n# receive the messages from the other client\nfor msg in client2.receive():\n    print(msg.text)\n```\n\n## Developing\n\n**Install dependencies**\n\n    poetry install\n\n**Run examples**\n\n    poetry run ./examples/simple-e2e.py\n\n**Run tests**\n\n    poetry run pytest\n\n**Run formatter**\n\n    poetry run black .\n',
    'author': 'Fetch.AI Limited',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
