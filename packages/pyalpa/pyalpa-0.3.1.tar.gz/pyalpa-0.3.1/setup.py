# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alpa', 'alpa.cli', 'alpa.config']

package_data = \
{'': ['*']}

install_requires = \
['alpa-conf>=0.3.1',
 'click>=8.0.0',
 'gitpython>=3.0',
 'pygithub>=1.4',
 'pyyaml>=5.0']

entry_points = \
{'console_scripts': ['alpa = alpa.cli.base:entry_point']}

setup_kwargs = {
    'name': 'pyalpa',
    'version': '0.3.1',
    'description': 'Integration tool with Alpa repository',
    'long_description': '## Alpa\n\nAnother cooL way to PAckage in copr\n\n### Status of alpa system\n\n| Package   | Copr build status                                                                                                                                                                                                     |\n| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |\n| alpa      | [![Copr build status](https://copr.fedorainfracloud.org/coprs/alpa-team/alpa/package/alpa/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/alpa-team/alpa/package/alpa/)                         |\n| alpa-conf | [![Copr build status](https://copr.fedorainfracloud.org/coprs/alpa-team/alpa/package/python-alpa-conf/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/alpa-team/alpa/package/python-alpa-conf/) |\n\n## Table of contents\n\n<!-- toc -->\n\n- [Requirements](#requirements)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Contributing](#contributing)\n\n<!-- tocstop -->\n\n### Requirements\n\n- linux OS\n- shell\n- at least python3.8\n- git\n\n### Installation\n\nFrom PyPi:\n\n```bash\n$ pip install --user pyalpa\n```\n\nFrom Copr:\n\n```bash\n$ dnf copr enable alpa-team/alpa\n$ dnf install alpa\n```\n\n### Usage\n\nTODO\n\n### Contributing\n\nTODO\n',
    'author': 'Jiri Kyjovsky',
    'author_email': 'j1.kyjovsky@gmail.com',
    'maintainer': 'Jiří Kyjovský',
    'maintainer_email': 'j1.kyjovsky@gmail.com',
    'url': 'https://github.com/alpa-team/alpa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
