# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['galilei', 'galilei.backends', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['fire==0.4.0',
 'flax>=0.6.4,<0.7.0',
 'jaxlib>=0.4.4,<0.5.0',
 'optax>=0.1.4,<0.2.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'tqdm>=4.65.0,<5.0.0']

extras_require = \
{'dev': ['tox>=3.24.5,<4.0.0',
         'virtualenv>=20.13.1,<21.0.0',
         'pip>=22.0.3,<23.0.0',
         'twine>=3.8.0,<4.0.0',
         'pre-commit>=2.17.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0',
         'mkdocs-material>=8.1.11,<9.0.0',
         'mkdocstrings>=0.18.0,<0.19.0',
         'mkdocs-autorefs>=0.3.1,<0.4.0',
         'mike>=1.1.2,<2.0.0'],
 'test': ['black>=22.3.0,<23.0.0',
          'isort==5.10.1',
          'flake8==4.0.1',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest>=7.0.1,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0']}

entry_points = \
{'console_scripts': ['galilei = galilei.cli:main']}

setup_kwargs = {
    'name': 'galilei',
    'version': '0.3.1',
    'description': 'the galilei project.',
    'long_description': '# galilei\n<a href="https://pypi.python.org/pypi/galilei">\n    <img src="https://img.shields.io/pypi/v/galilei.svg"\n        alt = "Release Status">\n</a>\n<a href="https://github.com/guanyilun/galilei/actions">\n    <img src="https://github.com/guanyilun/galilei/actions/workflows/release.yml/badge.svg?branch=master" alt="CI Status">\n</a>\n<a href="https://github.com/guanyilun/galilei/actions">\n    <img src="https://github.com/guanyilun/galilei/actions/workflows/dev.yml/badge.svg?branch=master" alt="CI Status">\n</a>\n<a href="https://guanyilun.github.io/galilei/">\n    <img src="https://img.shields.io/website/https/guanyilun.github.io/galilei/index.html.svg?label=docs&down_message=unavailable&up_message=available" alt="Documentation Status">\n</a>\n<a href="https://opensource.org/licenses/MPL-2.0">\n<img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">\n</a>\n<a href="https://zenodo.org/badge/latestdoi/594445054"><img src="https://zenodo.org/badge/594445054.svg" alt="DOI"></a>\n\n`galilei` is a python package that makes emulating a numerical functions easier and more composable. It supports multiple backends such as pytorch-based neural networks, GPy-based gaussian process regression, etc. As of now, it defaults to a jax+flax+optax backend which supports automatic differenciation of the emulated function and easy composibility with the rest of the jax-based eco-system.\n\nThe motivation of emulating a function is that sometimes computing a function could be a time consuming task, so one may need to find fast approximations of a function that\'s better than basic interpolation techniques. Machine learning techniques such as neural networks offer a solution to this problem which is generic enough to emulate any arbitrarily shaped function. In contrast to the original function, a neural-network based emulator runs blazingly fast and even more so with GPU, often achieveing over many orders of magnitude speed-up.\n\nThis idea of emulating function is not new. In the field of cosmology we have powerful tools such as\n[cosmopower](https://github.com/alessiospuriomancini/cosmopower) and its derived works such as [axionEmu](https://github.com/keirkwame/axionEmu), whose idea inspired this work. My aim in this work differs from the previous approach, as I intend to make a both generic and easily-composible function emulator that can take any arbitrary parametrized numerical function as an input, and return a function with the exact same signature as a drop-in replacement in existing code base, with no additional code changes needed. In addition, I also focus on making the emulated function automatically differenciable regardless of its original implementation.\n\n## Features\n- Support multiple backends: `torch`, `sklearn`, `gpy` (for gaussian process regression), `jax`.\n- Flexible: Able to emulate generic numerical functions.\n- Automatic differenciable (supported by selected backends): emulated function is automatically differenciable and easily composible with jax-based tools.\n- Easy to use: just add a decorator `@emulate` and use your emulated function as a drop-in replacement of your existing function in code-base without additional modification.\n- Allow arbitrary transformation of function output before training through the use of `Preconditioner`.\n\n\n## Installation\n```\npip install galilei\n```\n\n## Basic usage\nSuppose that we have an expensive function that we want to emulate\n```python\ndef myfun(a, b):\n    # assume this is a slow function\n    x = np.linspace(0, 10, 100)\n    return np.sin(a*x) + np.sin(b*x)\n```\nIf you want to emulate this function, you can simply add a decorator `@emulate` and supply the parameters that you want to evaluate this function at to build up the training data set.\n\n```python\nfrom galilei import emulate\n\n@emulate(samples={\n    \'a\': np.random.rand(1000),\n    \'b\': np.random.rand(1000)\n})\ndef myfun(a, b):\n    x = np.linspace(0, 10, 100)\n    return np.sin(a*x) + np.sin(b*x)\n```\nHere we are just making 1000 pairs of random numbers from 0 to 1 to train our function. When executing these lines, the emulator will start training, and once it is done, the original `myfun` function will be automatically replaced with the emulated version and should behave in the same way, except much faster!\n```\nTraining emulator...\n100%|██████████| 500/500 [00:09<00:00, 50.50it/s, loss=0.023]\nAve Test loss: 0.025\n```\n![Comparison](https://github.com/guanyilun/galilei/raw/master/data/demo.png)\n\nWith the default `jax` backend, the emulated function is automatically jax compatible, which means one can easily compose them with `jax` machinary, such as in example below where I have compiled the emulated function with `jit` and then vectorized it over its first argument with `vmap`.\n```python\nfrom jax import jit, vmap\n\nvmap(jit(myfun), in_axes=(0, None))(np.linspace(0, 1, 10), 0.5)\n```\nOutput:\n```\nArray([[-2.39813775e-02,  2.16133818e-02,  8.05920288e-02,\n         1.66035295e-01,  2.01425016e-01,  2.42054626e-01,\n         2.74079561e-01,  3.50277930e-01,  4.12616253e-01,\n         4.33193207e-01,  4.82740909e-01,  5.66871405e-01,\n         5.73131263e-01,  6.51429832e-01,  6.55564785e-01,\n         ...\n```\nThe emulated function will also be automatically differenciable regardless of the original implementation details. For example, we could easily evaluate its jacobian (without finite differencing) with\n```python\nfrom jax import jacfwd\n\njacfwd(myfun, argnums=(0,1))(0.2, 0.8)\n```\nOutput:\n```\n(Array([ 0.05104188,  0.18436229,  0.08595917,  0.06582363,  0.17270228, ...],      dtype=float32),\n Array([-3.3511031e-01,  1.2647966e-01,  4.3209594e-02,  2.4325712e-01, ...],      dtype=float32))\n```\nYou can also easily save your trained model with the `save` option\n```python\n@emulate(samples={\n    \'a\': np.random.rand(100),\n    \'b\': np.random.rand(100)\n}, backend=\'sklearn\', save="test.pkl")\ndef myfun(a, b):\n    x = np.linspace(0, 10, 100)\n    return np.sin(a*x) + np.sin(b*x)\n```\nand when you use it in production, simply load a pretrained model with\n```python\n@emulate(backend=\'sklearn\', load="test.pkl")\ndef myfun(a, b):\n    x = np.linspace(0, 10, 100)\n    return np.sin(a*x) + np.sin(b*x)\n```\nand your function will be replaced with a fast emulated version.\n![Comparison2](https://github.com/guanyilun/galilei/raw/master/data/demo2.png)\n\nIt\'s also possible to sample training points based on latin hypercube using the `build_samples` function. For example, here I build a 100 sample latin hypercube for a given range of `a` and `b`\n```python\nfrom galilei.sampling import build_samples\n@emulate(\n    samples=build_samples({"a": [0, 2], "b": [0, 2]}, 100),\n    backend=\'sklearn\'\n)\ndef myfun(a, b):\n    x = np.linspace(0, 10, 100)\n    return np.sin(a*x) + np.sin(b*x)\n```\nSometimes one might want to collect training data only instead of training the emulator. This could\nbe done by\n```python\nfrom galilei.experimental import collect\n\n@collect(\n    samples=build_samples({"a": [0, 2], "b": [0, 2]}, 100),\n    save="collection.pkl",\n    mpi=True\n)\ndef myfun(a, b):\n    x = np.linspace(0, 10, 100)\n    return np.sin(a*x) + np.sin(b*x)\n```\nwhich will save a precomputed collection to `collection.pkl` for future loading. Note that the option to use `mpi` depends on the user having a working `mpi4py` which needs to be installed by the user.\nThe collection could be loaded for training emulator using\n```python\n@emulate(\n    collection="collection.pkl",\n    backend=\'sklearn\'\n)\ndef myfunc(a, b):\n    raise Exception()\n\nmyfunc(1, 1)\n```\nsince the function will not be evaluated in this case, we note that the implementation of `myfunc` makes no difference (otherwise it would have given an error).\n\nFor more usage examples, see this notebook:\n<a href="https://colab.research.google.com/drive/1_pvuAIqLUz4gV1vxytueb7AMR6Jmx-8n?usp=sharing">\n<img src="https://user-content.gitlab-static.net/dfbb2c197c959c47da3e225b71504edb540e21d6/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667" alt="open in colab">\n</a>\n\n## Roadmap\n\n* TODO add prebuild preconditioners\n* TODO support downloading files from web\n* TODO auto infer backend\n* TODO chains of preconditioners\n\n## Credits\nThis package was created with the [ppw](https://zillionare.github.io/python-project-wizard) tool. For more information, please visit the [project page](https://zillionare.github.io/python-project-wizard/).\n\nIf this package is helpful in your work, please consider citing:\n```bibtex\n@article{yguan_2023,\n    title={galilei: a generic function emulator},\n    DOI={10.5281/zenodo.7651315},\n    publisher={Zenodo},\n    author={Yilun Guan},\n    year={2023},\n    month={Feb}}\n```\n\nFree software: MIT\n',
    'author': 'Yilun Guan',
    'author_email': 'zoom.aaron@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/guanyilun/galilei',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
