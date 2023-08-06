# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlt',
 'dlt.cli',
 'dlt.common',
 'dlt.common.configuration',
 'dlt.common.configuration.providers',
 'dlt.common.configuration.specs',
 'dlt.common.data_types',
 'dlt.common.data_writers',
 'dlt.common.destination',
 'dlt.common.json',
 'dlt.common.normalizers',
 'dlt.common.normalizers.json',
 'dlt.common.normalizers.naming',
 'dlt.common.reflection',
 'dlt.common.runners',
 'dlt.common.runtime',
 'dlt.common.schema',
 'dlt.common.storages',
 'dlt.destinations',
 'dlt.destinations.bigquery',
 'dlt.destinations.duckdb',
 'dlt.destinations.dummy',
 'dlt.destinations.postgres',
 'dlt.destinations.redshift',
 'dlt.extract',
 'dlt.helpers',
 'dlt.helpers.dbt',
 'dlt.load',
 'dlt.normalize',
 'dlt.pipeline',
 'dlt.reflection',
 'dlt.sources',
 'dlt.sources.helpers',
 'dlt.sources.helpers.requests']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1',
 'SQLAlchemy>=1.3.5',
 'astunparse>=1.6.3',
 'asyncstdlib>=3.10.5',
 'cachetools>=5.2.0',
 'click>=7.1',
 'cron-descriptor>=1.2.32',
 'gitpython>=3.1.29',
 'giturlparse>=0.10.0',
 'hexbytes>=0.2.2',
 'humanize>=4.4.0',
 'json-logging==1.4.1rc0',
 'makefun>=1.15.0',
 'pathvalidate>=2.5.2',
 'pendulum>=2.1.2',
 'pipdeptree>=2.3.3',
 'prometheus-client>=0.11.0',
 'pytz>=2022.6',
 'requests>=2.26.0',
 'requirements-parser>=0.5.0',
 'reretry>=0.11.8',
 'semver>=2.13.0',
 'sentry-sdk>=1.4.3',
 'setuptools>=65.6.0',
 'simplejson>=3.17.5',
 'tenacity>=8.2.2,<9.0.0',
 'tomlkit>=0.11.3',
 'tqdm>=4.64.1',
 'typing-extensions>=4.0.0',
 'tzdata>=2022.1']

extras_require = \
{':platform_python_implementation != "PyPy"': ['orjson>=3.8.6,<4.0.0'],
 'bigquery': ['grpcio>=1.50.0',
              'google-cloud-bigquery>=2.26.0',
              'pyarrow>=8.0.0'],
 'dbt': ['dbt-core>=1.3.0,<1.5.0',
         'dbt-redshift>=1.3.0,<1.5.0',
         'dbt-bigquery>=1.3.0,<1.5.0',
         'dbt-duckdb>=1.3.0,<1.5.0'],
 'duckdb': ['duckdb>=0.6.1,<0.8.0'],
 'gcp': ['grpcio>=1.50.0', 'google-cloud-bigquery>=2.26.0', 'pyarrow>=8.0.0'],
 'postgres': ['psycopg2-binary>=2.9.1'],
 'postgres:platform_python_implementation == "PyPy"': ['psycopg2cffi>=2.9.0'],
 'redshift': ['psycopg2-binary>=2.9.1'],
 'redshift:platform_python_implementation == "PyPy"': ['psycopg2cffi>=2.9.0']}

entry_points = \
{'console_scripts': ['dlt = dlt.cli._dlt:_main']}

setup_kwargs = {
    'name': 'python-dlt',
    'version': '0.2.0a29',
    'description': 'DLT is an open-source python-native scalable data loading framework that does not require any devops efforts to run.',
    'long_description': '![](https://github.com/dlt-hub/dlt/raw/devel/docs/DLT-Pacman-Big.gif)\n\n<p align="center">\n\n[![PyPI version](https://badge.fury.io/py/python-dlt.svg)](https://pypi.org/project/python-dlt/)\n[![LINT Badge](https://github.com/dlt-hub/dlt/actions/workflows/lint.yml/badge.svg)](https://github.com/dlt-hub/dlt/actions/workflows/lint.yml)\n[![TEST COMMON Badge](https://github.com/dlt-hub/dlt/actions/workflows/test_common.yml/badge.svg)](https://github.com/dlt-hub/dlt/actions/workflows/test_common.yml)\n[![TEST DESTINATIONS Badge](https://github.com/dlt-hub/dlt/actions/workflows/test_destinations.yml/badge.svg)](https://github.com/dlt-hub/dlt/actions/workflows/test_destinations.yml)\n[![TEST BIGQUERY Badge](https://github.com/dlt-hub/dlt/actions/workflows/test_destination_bigquery.yml/badge.svg)](https://github.com/dlt-hub/dlt/actions/workflows/test_destination_bigquery.yml)\n[![TEST DBT Badge](https://github.com/dlt-hub/dlt/actions/workflows/test_dbt_runner.yml/badge.svg)](https://github.com/dlt-hub/dlt/actions/workflows/test_dbt_runner.yml)\n\n\n</p>\n\n# data load tool (dlt)\n\n**data load tool (dlt)** is a simple, open source Python library that makes data loading easy\n- Automatically turn the JSON returned by any API into a live dataset stored wherever you want it\n- `pip install python-dlt` and then include `import dlt` to use it in your Python loading script\n- The **dlt** library is licensed under the Apache License 2.0, so you can use it for free forever\n\nRead more about it on the [dlt Docs](https://dlthub.com/docs)\n\n# semantic versioning\n`python-dlt` will follow the semantic versioning with [`MAJOR.MINOR.PATCH`](https://peps.python.org/pep-0440/#semantic-versioning) pattern. Currently we do **pre-release versioning** with major version being 0.\n- `minor` version change means breaking changes\n- `patch` version change means new features that should be backward compatible\n- any suffix change ie. `a10` -> `a11` is a patch\n\n# development\n`python-dlt` uses `poetry` to manage, build and version the package. It also uses `make` to automate tasks. To start\n```sh\nmake install-poetry  # will install poetry, to be run outside virtualenv\n```\nthen\n```sh\nmake dev  # will install all deps including dev\n```\nExecuting `poetry shell` and working in it is very convenient at this moment.\n\n## python version\nUse python 3.8 for development which is the lowest supported version for `python-dlt`. You\'ll need `distutils` and `venv`:\n\n```shell\nsudo apt-get install python3.8\nsudo apt-get install python3.8-distutils\nsudo apt install python3.8-venv\n```\nYou may also use `pyenv` as [poetry](https://python-poetry.org/docs/managing-environments/) suggests.\n\n## bumping version\nPlease use `poetry version prerelease` to bump patch and then `make build-library` to apply changes. The source of the version is `pyproject.toml` and we use poetry to manage it.\n\n## testing and linting\n`python-dlt` uses `mypy` and `flake8` with several plugins for linting. We do not reorder imports or reformat code.\n\n`pytest` is used as test harness. `make test-common` will run tests of common components and does not require any external resources.\n\n### testing destinations\nTo test destinations use `make test`. You will need following external resources\n1. `BigQuery` project\n2. `Redshift` cluster\n3. `Postgres` instance. You can find a docker compose for postgres instance [here](tests/load/postgres/docker-compose.yml). When run the instance is configured to work with the tests.\n```shell\ncd tests/load/postgres/\ndocker-compose up --build -d\n```\n\nSee `tests/.example.env` for the expected environment variables and command line example to run the tests. Then create `tests/.env` from it. You configure the tests as you would configure the dlt pipeline.\nWe\'ll provide you with access to the resources above if you wish to test locally.\n\nTo test local destinations (`duckdb` and `postgres`) run `make test-local`. You can run this tests without additional credentials (just copy `.example.env` into `.env`)\n\n## publishing\n\n1. Make sure that you are on `devel` branch and you have the newest code that passed all tests on CI.\n2. Verify the current version with `poetry version`\n3. You\'ll need `pypi` access token and use `poetry config pypi-token.pypi your-api-token` then\n```\nmake publish-library\n```\n4. Make a release on github, use version and git tag as release name\n\n## contributing\n\nTo contribute via pull request:\n1. Create an issue with your idea for a feature etc.\n2. Write your code and tests\n3. Lint your code with `make lint`. Test the common modules with `make test-common`\n4. If you work on a destination code then contact us to get access to test destinations\n5. Create a pull request\n',
    'author': 'dltHub Inc.',
    'author_email': 'services@dlthub.com',
    'maintainer': 'Marcin Rudolf',
    'maintainer_email': 'marcin@dlthub.com',
    'url': 'https://github.com/dlt-hub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
