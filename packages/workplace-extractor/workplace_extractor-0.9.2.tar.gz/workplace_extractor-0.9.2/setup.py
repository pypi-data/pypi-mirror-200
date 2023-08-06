# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['workplace_extractor',
 'workplace_extractor.Extractors',
 'workplace_extractor.Nodes']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4.0',
 'asyncio>=3.4,<4.0',
 'matplotlib>=3.4.2,<4.0.0',
 'networkx>=2.5.1,<3.0.0',
 'numpy>=1.20,<2.0',
 'pandas>=1.2,<2.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'workplace-extractor',
    'version': '0.9.2',
    'description': 'Extract data created in a corporate Workplace by Facebook installation using the Graph/SCIM APIs',
    'long_description': '# Workplace Extractor\n<p style="float: right;">\n  <b>Python package to extract posts from</b>\n  <img src="https://raw.githubusercontent.com/denisduarte/midia/main/workplace.png" width="100" height="24">\n  <img src="https://raw.githubusercontent.com/denisduarte/midia/main/from_facebook.png" width="100" height="9">\n</p>\n\n# Overview\nThe Workplace Extractor package was written to allow a complete extraction of posts form a Workplace installation. It provides the following key features:\n\n* Access to the SCIM and GRAPH API provided by Facebook;\n* Asyncronous calls to increase speed;\n* Lists of **posts**, **members**, **groups**, **comments**, **event attendees** are exported to CSV files;\n* A ranking of most relevant members can be created based on the number of interctions (comments and reactions)\n* The interaction network can be wxported to a GEXF file;\n\n# Usage\n\n### Installation\nTo get the Workplace Extractor package, either fork this github repo or use Pypi via pip.\n```sh\n$ pip install workplace_extractor\n```\n### How to use it\n\nYou can simple run a python script with the code below:\n\n```sh\nimport workplace_extractor\n\nworkplace_extractor.run()\n```\n\n\nThis package uses [argparse](https://docs.python.org/3/library/argparse.html) and [Gooey](https://github.com/chriskiehl/Gooey) to create an end-user-friendly front end GUI application. Just run the app and a dialog will show up asking for the input parameters.\n\nThe application will offer some extraction options:\n\n1. **POSTS** - used for extracting all posts published in a given period of time or feed, from a given author etc.\n\n    <img src="https://raw.githubusercontent.com/denisduarte/midia/main/Workplace%20App%201%20-%20Posts.png" width="402" height="337">\n\n\n2. **Comments** - used for extracting all comments made in a post.\n\n    <img src="https://raw.githubusercontent.com/denisduarte/midia/main/Workplace%20App%202%20-%20Comments.png" width="402" height="337">\n\n\n3. **People** - used for extracting all Workplace users.\n\n    <img src="https://raw.githubusercontent.com/denisduarte/midia/main/Workplace%20App%203%20-%20People.png" width="402" height="337">\n\n\n4. **Groups** - used for all groups.\n\n    <img src="https://raw.githubusercontent.com/denisduarte/midia/main/Workplace%20App%204%20-%20Groups.png" width="402" height="337">\n\n\n5. **Members** - used for extracting all members of a group\n\n    <img src="https://raw.githubusercontent.com/denisduarte/midia/main/Workplace%20App%205%20-%20Members.png" width="402" height="337">\n\n6. **Attendees** - used for extracting all attendees of an event.\n\n    <img src="https://raw.githubusercontent.com/denisduarte/midia/main/Workplace%20App%206%20-%20Attendees.png" width="402" height="337">\n\n7. **Interactions** - used for extracting interactions among all workplace users. This option can be used can be used with a network visualization solution, such as [Gephi](https://gephi.org/), for further analysis.\n\n    <img src="https://raw.githubusercontent.com/denisduarte/midia/main/Workplace%20App%207%20-%20Interactions.png" width="402" height="337">\n\n\n**You must have an access token with full access to both SCIM and GRAPH API in order to the extraction to work**\n\nA config.ini file con be used to set some key parameters. Two required ones are:\n\n* **output_dir** - path the folder where the output will be stored\n* **access_token** - path to a file containing the Workplace access token\n\n# Warning\nAs many http calls are made during the export process, your program may take a while to finish, depending on the size of your Workplace installation. As a reference, on an installation with around 85,000 users, 3,000 groups and 110,000 posts the exectution takes around 4 hours to complete.\n\n# License\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nCopyright 2021 Denis Duarte\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n\n',
    'author': 'Denis Duarte',
    'author_email': 'den.duarte@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/denisduarte/workplace_extractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
