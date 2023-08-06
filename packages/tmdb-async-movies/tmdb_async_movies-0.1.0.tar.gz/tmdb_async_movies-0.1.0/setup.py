# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tmdb_async_movies']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-retry>=2.8.3,<3.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'click>=8.0.1',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['tmdbasyncmovies = tmdb_async_movies.cli:tmdbasyncmovies']}

setup_kwargs = {
    'name': 'tmdb-async-movies',
    'version': '0.1.0',
    'description': 'tmdb_async_movies',
    'long_description': '# tmdb-async-movies\n\n[![PyPI](https://img.shields.io/pypi/v/tmdb-async-movies.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/tmdb-async-movies.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/tmdb-async-movies)][python version]\n[![License](https://img.shields.io/pypi/l/tmdb-async-movies)][license]\n\n[![Read the documentation at https://tmdb-async-movies.readthedocs.io/](https://img.shields.io/readthedocs/tmdb-async-movies/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/tilschuenemann/tmdb-async-movies/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/tilschuenemann/tmdb-async-movies/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/tmdb-async-movies/\n[status]: https://pypi.org/project/tmdb-async-movies/\n[python version]: https://pypi.org/project/tmdb-async-movies\n[read the docs]: https://tmdb-async-movies.readthedocs.io/\n[tests]: https://github.com/tilschuenemann/tmdb-async-movies/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/tilschuenemann/tmdb-async-movies\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n`tmdb-async-movies` is an asynchronous utility for fetching bulk movie data from [TMDB](https://www.themoviedb.org/) using movie title and optionally release year.\n\n- Designed for bulk usage: Pipe in a list of queries and get results immediately.\n- Blazing fast: Asynchronous calls enable you to get metadata from hundreds of movies in a couple of seconds.\n- Typed: Metadata dataframes are strictly cast so you don\'t have to do it yourself.\n- Hackable: It\'s a small project with ~500 LOC.\n- Accessible: It has both a Python API and a CLI.\n\n## Requirements\n\nYou\'ll need to have a TMDB API key in order to make API requests.\n\nDefault environment variable:\n\n```bash\n$ export TMDB_API_KEY="your_api_key_here"\n```\n\nPython:\n\n```python\nfrom tmdb_async_movies.main import TmdbAsyncMovies\nt = TmdbAsyncMovies(tmdb_api_key="your_api_key_here")\n```\n\nCLI:\n\n```bash\ntmdb-async-movies -t "your_api_key_here" from_input "1999 The Matrix"\n```\n\n## Installation\n\nYou can install _tmdb-async-movies_ via [pip] from [PyPI]:\n\n```console\n$ pip install tmdb-async-movies\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_tmdb_async_movies_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/tilschuenemann/tmdb-async-movies/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/tilschuenemann/tmdb-async-movies/blob/main/LICENSE\n[contributor guide]: https://github.com/tilschuenemann/tmdb-async-movies/blob/main/CONTRIBUTING.md\n[command-line reference]: https://tmdb-async-movies.readthedocs.io/en/latest/cli.html\n',
    'author': 'Til Schünemann',
    'author_email': 'til.schuenemann@mailbox.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tilschuenemann/tmdb-async-movies',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
