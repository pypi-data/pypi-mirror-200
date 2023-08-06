# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['WinSCPPasswdExtractor']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['WinSCPPasswdExtractor = '
                     'WinSCPPasswdExtractor.WinSCPPasswdExtractor:run']}

setup_kwargs = {
    'name': 'winscppasswdextractor',
    'version': '1.0.0',
    'description': 'Extract WinSCP Credentials from any Windows System or winscp config file',
    'long_description': '# WinSCP Password Extractor\nWinSCP stores ssh session passwords in an encoded format in either the registry or a file called WinSCP.ini.\nThis python script searches in the winscp default locations to extract stored credentials.\n\nThese default file locations are:\n- %APPDATA%\\WinSCP.ini\n- %USER%\\Documents\\WinSCP.ini\n\n## Usage\nYou can either specify a file path if you know the exact path to an existing WinSCP.ini file or you let the tool itself look if any credentials are stored in the default locations.\n```python3\npython WinSCPPwdDump.py\npython WinSCPPwdDump.py <path-to-file>\n```\n\n## About\nThis Tool is based on the work of [winscppasswd](https://github.com/anoopengineer/winscppasswd), the ruby winscp parser from [Metasploit-Framework](https://github.com/rapid7/metasploit-framework) and the awesome work from [winscppassword](https://github.com/dzxs/winscppassword).\n\nThey did the hard stuff\n',
    'author': 'Alexander Neff',
    'author_email': 'alex99.neff@gmx.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
