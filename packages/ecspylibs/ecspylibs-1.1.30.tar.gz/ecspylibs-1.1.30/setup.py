# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ecspylibs']

package_data = \
{'': ['*']}

install_requires = \
['Autologging>=1.3.2,<2.0.0',
 'PyYAML>=6.0,<7.0',
 'lxml==4.5.2',
 'numpy==1.19.1',
 'pandas==1.0.5',
 'psutil==5.7.2',
 'pycrypto>=2.6.1,<3.0.0',
 'requests>=2.28.2,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'urllib3>=1.26.15,<2.0.0',
 'xlrd==1.2.0']

setup_kwargs = {
    'name': 'ecspylibs',
    'version': '1.1.30',
    'description': 'Local python libraries used across multiple programs.',
    'long_description': '# ECSpylibs\n\n# Package files\n    -rw-r--r--. 1 tom tom 2568 Feb  2 13:57 src/ecspylibs/buildfunctionlist.py\n    -rw-r--r--. 1 tom tom 8390 Feb  2 13:57 src/ecspylibs/checkservice.py\n    -rw-r--r--. 1 tom tom 3090 Feb  2 13:57 src/ecspylibs/cleanuptempdirs.py\n    -rw-r--r--. 1 tom tom 6123 Mar 16 17:03 src/ecspylibs/configfile.py\n    -rw-r--r--. 1 tom tom  465 Jan 26 11:05 src/ecspylibs/__init__.py\n    -rw-r--r--. 1 tom tom 3678 Feb  2 13:57 src/ecspylibs/initsetup.py\n    -rw-r--r--. 1 tom tom 1676 Feb  8 12:50 src/ecspylibs/parallel.py\n    -rw-r--r--. 1 tom tom 4965 Feb  2 13:57 src/ecspylibs/parseemail.py\n    -rw-r--r--. 1 tom tom 3644 Feb  2 13:57 src/ecspylibs/parsexml.py\n    -rw-r--r--. 1 tom tom 3650 Feb  2 13:57 src/ecspylibs/password.py\n    -rw-r--r--. 1 tom tom 1879 Feb  2 13:57 src/ecspylibs/reapchildren.py\n    -rw-r--r--. 1 tom tom 2993 Feb  2 13:57 src/ecspylibs/sendemail.py\n\n# Git information\n[GIT Home][ECSPYLIBS],\n[README File][README],\n[LICENSE File][LICENSE],\n[ChangeLog File][CHANGELOG],\n[pyproject.toml File][PYPROJECT].\n\n# About Me\n[My contact information][About Me].\n\n[ECSPYLIBS]: https://git.wayne.edu/ECS_Projects/ECSpylibs\n[README]: https://git.wayne.edu/ECS_Projects/ECSpylibs/-/blob/master/README.md\n[LICENSE]: https://git.wayne.edu/ECS_Projects/ECSpylibs/-/blob/master/LICENSE.txt\n[CHANGELOG]: https://git.wayne.edu/ECS_Projects/ECSpylibs/-/blob/master/ChangeLog\n[PYPROJECT]: https://git.wayne.edu/ECS_Projects/ECSpylibs/-/blob/master/pyproject.toml\n[About Me]: https://About.Me/Thomas.R.Stevenson\n',
    'author': 'Thomas R. Stevenson',
    'author_email': 'aa0026@wayne.edu',
    'maintainer': 'Thomas R. Stevenson',
    'maintainer_email': 'aa0026@wayne.edu',
    'url': 'https://git.wayne.edu/ECS_Projects/ECSpylibs.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
