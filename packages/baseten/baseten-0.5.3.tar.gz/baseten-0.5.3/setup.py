# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baseten',
 'baseten.client_commands',
 'baseten.common',
 'baseten.models',
 'baseten.training']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'click>=7.0',
 'colorama>=0.4.3',
 'coolname>=1.1.0',
 'halo>=0.0.31,<0.0.32',
 'jinja2>=2.10.3',
 'joblib>=0.12.5',
 'pytz>=2022.7.1,<2023.0.0',
 'pyyaml>=5.1',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.22',
 'semantic-version>=2.10.0,<3.0.0',
 'single-source>=0.3.0,<0.4.0',
 'tenacity>=8.0.1,<9.0.0',
 'tqdm>=4.62.1,<5.0.0',
 'truss>=0.4.0,<0.5.0',
 'types-pillow>=9.3.0.4,<10.0.0.0',
 'types-pytz>=2022.7.1.0,<2023.0.0.0',
 'types-pyyaml>=6.0.12.2,<7.0.0.0',
 'types-requests>=2.28.11.7,<3.0.0.0',
 'types-setuptools>=65.6.0.2,<66.0.0.0']

entry_points = \
{'console_scripts': ['baseten = baseten.cli:cli_group']}

setup_kwargs = {
    'name': 'baseten',
    'version': '0.5.3',
    'description': 'Deploy machine learning models to Baseten',
    'long_description': "# Baseten\n\nThis is the Python client for [Baseten](https://baseten.co) and [Blueprint](https://blueprint.baseten.co).\n\n## Installation\n\nInstall the latest version of the `baseten` package:\n\n```sh\npip install --upgrade baseten\n```\n\n## Baseten\n\nBaseten is a hosted platform for building ML-powered applications. Build apps with auto-scaling, GPU access, CRON jobs, and serverless functions.\n\nVisit our official documentation for Baseten at [docs.baseten.co](https://docs.baseten.co).\n\n## Blueprint\n\nBlueprint is the model fine-tuning and serving infrastructure for developers. It's powered by Baseten infrastructure and uses the baseten PyPi package.\n\nVisit our official documentation for Blueprint at [docs.blueprint.baseten.co](https://docs.blueprint.baseten.co).",
    'author': 'Amir Haghighat',
    'author_email': 'amir@baseten.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
