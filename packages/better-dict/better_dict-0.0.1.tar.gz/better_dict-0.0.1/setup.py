# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['better_dict']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.10b0',
 'flake8-bandit>=2.1.2',
 'flake8-bugbear>=21.9.2',
 'flake8-docstrings>=1.6.0',
 'flake8-rst-docstrings>=0.2.5',
 'flake8>=4.0.1',
 'joblib>=1.2.0,<2.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pytest>=7.2.2,<8.0.0',
 'python-dotenv>=0.19.2,<0.20.0']

extras_require = \
{':python_full_version >= "3.6.2"': ['flake8-annotations>=2.7.0,<3.0.0']}

setup_kwargs = {
    'name': 'better-dict',
    'version': '0.0.1',
    'description': 'Python dictionary revamped.',
    'long_description': '![](docs/_static/EY_logo_5.gif)\n\n# Better Dict\n\n[![PyPI](https://img.shields.io/pypi/v/better-dict.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/better-dict.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/better-dict)][python version]\n[![License](https://img.shields.io/pypi/l/better-dict)][license]\n[![Read the documentation at https://better-dict.readthedocs.io/](https://img.shields.io/readthedocs/better-dict/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Codecov](https://codecov.io/gh/ingwersen-erik/better-dict/branch/main/graph/badge.svg)][codecov]\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit\\&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/better-dict/\n\n[status]: https://pypi.org/project/better-dict/\n\n[python version]: https://pypi.org/project/better-dict\n\n[read the docs]: https://better-dict.readthedocs.io/\n\n[tests]: https://github.com/ingwersen-erik/better-dict/actions?workflow=Tests\n\n[codecov]: https://app.codecov.io/gh/ingwersen-erik/better-dict\n\n[pre-commit]: https://github.com/pre-commit/pre-commit\n\n[black]: https://github.com/psf/black\n\n## Description\n\nPython dictionary on steroids. The custom dictionary is inspired in\nby the functionalities that [pandas](https://pandas.pydata.org/) offers in\ntheir `DataFrame` and `Series` classes.\n\n***\n\n## Installation\n\nTo install **Better Dict**, execute the command:\n\n```console\n$ pip install better-dict\n```\n\n## Quickstart\n\nHere\'s a quick example of how to use **Better Dict**:\n\n```python\nimport better_dict as bd\n\nd = bd.BetterDict({"a": 1, "b": 2, "c": 3})\n\n# == Accessing values ==========================================================\n# Access multiple keys at once:\nd[["a", "b"]]  # returns {"a": 1, "b": 2}\n\n# Access dictionary values using item indexes:\nd.iloc[0]       # returns 1\nd.iloc[[0, 2]]  # returns [1, 3]\nd.iloc[1:]      # returns [2, 3]\n\n# Access dictionary keys using their values:\nd.vloc[1]       # returns "a"\nd.vloc[[1, 3]]  # returns ["a", "c"]\n\n# == Key Translations ==========================================================\n# Rename dictionary keys:\nd.rename({"a": "A", "b": "B", "c": "C"})    # returns {"A": 1, "B": 2, "C": 3}\n\n# == Apply Function ============================================================\n# Apply a function to all dictionary values:\nd.apply(lambda x: x + 1)                    # returns {"a": 2, "b": 3, "c": 4}\n\n# Apply a function to all dictionary keys:\nd.apply_keys(lambda x: x.upper(), axis=0)   # returns {"A": 1, "B": 2, "C": 3}\n\n# == I/O Operations ============================================================\n# Save dictionary to a Pickle file:\nd.to_pickle("d.pkl")\n\n# Load dictionary from a Pickle file:\nd = bd.BetterDict.from_pickle("d.pkl")\n\n# Save dictionary to a joblib file:\nd.to_joblib("d.joblib")\n\n# Load dictionary from a joblib file:\nd = bd.BetterDict.from_joblib("d.joblib")\n```\n\n## Q&A\n\n### 1. What is the ``BetterDict`` class and what additional functionality does it provide?\n\nThe ``BetterDict`` class is a custom subclass of Python\'s built-in dict class,\ndesigned to provide additional functionality for easier and more flexible\nmanipulation of dictionaries. The main enhancements include:\n\n* Accessing dictionary keys by value.\n* Manipulating dictionary keys and values using index notation.\n* Accessing and manipulating dictionary values using dot notation.\n* Other features include saving/loading dictionaries to/from files, creating\n  dictionaries from various data structures, applying functions to\n  dictionary values and keys, fuzzy key matching, and renaming dictionary keys.\n\n### 2. How can I access and set values in a ``BetterDict`` instance?\n\nAccessing and setting values in a ``BetterDict`` instance is made easy through a\nvariety of methods:\n\n* **``Get``/``Set`` values by key:** Use the standard dictionary syntax with square\nbrackets (e.g., ``d["key"]`` and ``d["key"] = value``).\n* **Get/Set multiple values at once:** Supply an iterable of keys\n  (e.g., ``d["key1", "key2"]`` and ``d["key1", "key2"] = value1, value2``).\n* **Index notation:** Use the iloc property to access and set values by index\n  (e.g., ``d.iloc[index]`` and ``d.iloc[index1, index2] = value1, value2``).\n* Additionally, dot notation can be used to access and set values (e.g., `d.key` and `d.key = value`).\n\n### 3. What are the available I/O operations for ``BetterDict`` and how can I use them?\n\n``BetterDict`` supports I/O operations using the **pickle** and **joblib** libraries,\nallowing you to easily save and load dictionaries to/from files. The main\nmethods for I/O operations are:\n\n* **Save with pickle:** Use the `save_pickle` method, supplying the file path\n  (e.g., `d.save_pickle("file_path.pkl")`).\n* **Load with pickle:** Use the `load_pickle` method, supplying the file path\n  (e.g., ``d = BetterDict.load_pickle("file_path.pkl"))``.\n* **Save with joblib:** Use the `save_joblib` method, supplying the file path\n  (e.g., `d.save_joblib("file_path.joblib")`).\n* **Load with joblib:** Use the `load_joblib` method, supplying the file path\n  (e.g., ``d = BetterDict.load_joblib("file_path.joblib")``).\n\n### 4. How can I create a ``BetterDict`` from different data structures like `pandas.DataFrame` or `numpy.ndarray`?\n\n``BetterDict`` offers class methods to create instances from various data\nstructures, such as pandas DataFrames, pandas Series, numpy arrays, and lists:\n\n- **From `pandas.DataFrame`:** Use the `from_frame` method (e.g., ``d = BetterDict.from_frame(data_frame))``.\n- **From `pandas.Series`:** Use the `from_series` method (e.g., ``d = BetterDict.from_series(data_series))``.\n- **From `numpy.ndarray`:** No direct method is available, but you can first convert the array to a pandas DataFrame and then use `from_frame`\n  (e.g., ``d = BetterDict.from_frame(pd.DataFrame(array)))``.\n- **From list:** Use the `from_list` method (e.g., ``d = BetterDict.from_list(list_obj))``.\n\nThese methods facilitate easy conversion between different data structures and ``BetterDict``.\n\n## Contributing\n\nContributions are welcome! If you have any suggestions or feature requests,\nplease open an issue or submit a pull request.\n\nFor more information on how to contribute to **Better Dict**,\nplease read the [Contributor Guide](./CONTRIBUTING.md).\n\n## License\n\nDistributed under the terms of the [MIT License](./LICENSE),\n*Better Dict* is free and open source software.\n\n<!-- github-only -->\n\n[license]: https://github.com/ingwersen-erik/better-dict/blob/main/LICENSE\n\n[contributor guide]: https://github.com/ingwersen-erik/better-dict/blob/main/CONTRIBUTING.md\n\n[command-line reference]: https://better-dict.readthedocs.io/en/latest/usage.html\n',
    'author': 'Erik Ingwersen',
    'author_email': 'erik.ingwersen@br.ey.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ingwersen-erik/better-dict',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
