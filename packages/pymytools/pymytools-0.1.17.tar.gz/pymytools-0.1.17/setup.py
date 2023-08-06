# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymytools', 'pymytools.special']

package_data = \
{'': ['*'], 'pymytools': ['assets/sounds/*']}

install_requires = \
['h5py>=3.8.0,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pyevtk>=1.5.0,<2.0.0',
 'pymyplot>=0.2.7,<0.3.0',
 'rich>=13.3.2,<14.0.0',
 'scipy>=1.10.1,<2.0.0',
 'simpleaudio>=1.0.4,<2.0.0',
 'tensorboard>=2.12.0,<3.0.0',
 'torch>=2.0.0,<3.0.0',
 'tqdm>=4.65.0,<5.0.0',
 'vtk>=9.2.6,<10.0.0']

setup_kwargs = {
    'name': 'pymytools',
    'version': '0.1.17',
    'description': 'Tools used in my pystops project.',
    'long_description': '# Collection of Useful Tools for `pystops` Project\n\nDuring my PhD, I noticed that some features that I implemented throughout my projects appeared repeatedly.\nAs a result, I decided to separate these features and manage them appropriately.\n\n## Goal\n\nManage/unify fragmented features and deploy to `pypi.org`.\n\n## Features\n\n- Diagnostics\n  - file I/O\n    - Supports: `csv`, `hdf5` (`.h5`), and `vtk` (both `.vti` and `.vtu`) formats\n    - All data loaded are `torch.Tensor`\n  - Tensorboard tracker\n- Logging, timer, and progress bar\n  - Prettier representation using `rich` package\n\n## Dependencies\n\nMain dependencies:\n\n- `python = "^3.10"`\n- `h5py = "^3.8.0"`\n- `pyevtk = "^1.5.0"`\n- `rich = "^13.3.2"`\n- `tensorboard = "^2.12.0"`\n- `tqdm = "^4.65.0"`\n- `pandas = "^1.5.3"`\n- `torch = "^1.13.1"`\n- `vtk = "^9.2.6"`\n\nMy other personal project:\n\n- `pymyplot = "^0.2.7"` (for plotting)\n',
    'author': 'Kyoungseoun Chung',
    'author_email': 'kyoungseoun.chung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
