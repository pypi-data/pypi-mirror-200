# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cta']
install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'feedgen>=0.9.0,<0.10.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'car-talk-archiver',
    'version': '1.0.4',
    'description': '',
    'long_description': '# Car Talk Archiver\n\nA script that generates an RSS XML feed containing every Car Talk episode currently hosted by NPR, dating back to 2007. Host via HTTP and update with a program like crontab for maximum effect.\n\nCompatible with any podcast application that supports RSS.\n\n## Requirements\n```\npython = "^3.10"\nbeautifulsoup4 = "^4.11.2"\nfeedgen = "^0.9.0"\nrequests = "^2.28.2"\n```\n\n## Installation\n```\npip install car-talk-archiver\n```\n\n## Usage\n```\nusage: cta.py [-h] [-i file] [-o file]\n\nGenerate a podcast RSS feed containing every Car Talk episode currently hosted by NPR.\n\noptions:\n  -h, --help            show this help message and exit\n  -i file, --input file\n                        file name of an existing feed (if specified, script will only check for newer episodes)\n  -o file, --output file\n                        output file name (defaults to cartalk_<timestamp>.xml in current working directory)\n```\n\n## Examples\nGenerate a new feed:\n```\n$ ./cta.py\n```\n\nUse an existing feed to generate a new feed including the most recent episodes:\n```\n$ ./cta.py -i cartalk.xml\n```\n\nUpdate and overwrite an existing feed with the most recent episodes:\n```\n$ ./cta.py -i cartalk.xml -o cartalk.xml\n```',
    'author': 'Brett Heinkel',
    'author_email': 'bheinks@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bheinks/car-talk-archiver',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
