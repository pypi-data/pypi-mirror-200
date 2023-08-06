# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apply_async']

package_data = \
{'': ['*']}

install_requires = \
['multiprocess>=0.70.14,<0.71.0', 'rich>=13.3.3,<14.0.0']

setup_kwargs = {
    'name': 'apply-async',
    'version': '0.1.1',
    'description': '',
    'long_description': '# apply_async\n\nIf you have a large number of files and you need to apply a function to each of them to get some outputs, then this is for you.\n\nThis provides a function called `apply_async` which takes in a list of filenames and a function to apply, and does the following for you:\n\n- batches the files\n- applies your function to each batch asynchronously\n- controls the number of batches to process at a time, and automatically adds new batches when old ones complete\n- shows a progress bar for each batch\n\n## Installation\n\nFrom pip:\n\n```bash\npip install apply_async\n```\n\nLatest version (from source):\n\n```bash\npip install "git+https://github.com/al-jshen/apply_async"\n```\n\n## Demo\n\n<img width="656" alt="Screenshot 2023-03-29 at 6 26 16 PM" src="https://user-images.githubusercontent.com/22137276/228681583-98f65227-68fe-472a-a3e1-ab320bdb60cb.png">\n\n',
    'author': 'Jeff Shen',
    'author_email': 'shenjeff@princeton.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
