# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kilroy_face_debug',
 'kilroy_face_debug.resources',
 'kilroy_face_debug.scoring']

package_data = \
{'': ['*']}

install_requires = \
['detoxify>=0.5,<0.6',
 'kilroy-face-server-py-sdk>=0.9,<0.10',
 'numpy>=1.23,<2.0',
 'omegaconf>=2.2,<3.0',
 'platformdirs>=2.5,<3.0',
 'pydantic[dotenv]>=1.10,<2.0',
 'tweetnlp>=0.4,<0.5',
 'typer[all]>=0.6,<0.7']

entry_points = \
{'console_scripts': ['kilroy-face-debug = kilroy_face_debug.__main__:cli',
                     'kilroy-face-debug-fetch-models = '
                     'kilroy_face_debug.models:fetch_models']}

setup_kwargs = {
    'name': 'kilroy-face-debug',
    'version': '0.2.0',
    'description': 'kilroy face for Debug 🎮',
    'long_description': '<h1 align="center">kilroy-face-debug</h1>\n\n<div align="center">\n\nkilroy face for debugging 🧪\n\n[![Lint](https://github.com/kilroybot/kilroy-face-debug/actions/workflows/lint.yaml/badge.svg)](https://github.com/kilroybot/kilroy-face-debug/actions/workflows/lint.yaml)\n[![Multiplatform tests](https://github.com/kilroybot/kilroy-face-debug/actions/workflows/test-multiplatform.yaml/badge.svg)](https://github.com/kilroybot/kilroy-face-debug/actions/workflows/test-multiplatform.yaml)\n[![Docker tests](https://github.com/kilroybot/kilroy-face-debug/actions/workflows/test-docker.yaml/badge.svg)](https://github.com/kilroybot/kilroy-face-debug/actions/workflows/test-docker.yaml)\n[![Docs](https://github.com/kilroybot/kilroy-face-debug/actions/workflows/docs.yaml/badge.svg)](https://github.com/kilroybot/kilroy-face-debug/actions/workflows/docs.yaml)\n\n</div>\n\n---\n\n## Installing\n\nUsing `pip`:\n\n```sh\npip install kilroy-face-debug\n```\n\n## Usage\n\nTo run the face server, install the package and run the following command:\n\n```sh\nkilroy-face-debug\n```\n\nThis will start the face server on port 9999 by default.\nThen you can communicate with the server, for example by using\n[this package](https://github.com/kilroybot/kilroy-face-client-py-sdk).\n',
    'author': 'kilroy',
    'author_email': 'kilroymail@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kilroybot/kilroy-face-debug',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
