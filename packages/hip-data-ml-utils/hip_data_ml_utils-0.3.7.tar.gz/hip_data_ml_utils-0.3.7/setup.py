# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hip_data_ml_utils',
 'hip_data_ml_utils.core',
 'hip_data_ml_utils.mlflow_databricks',
 'hip_data_ml_utils.pyathena_client']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0',
 'aiobotocore==2.4.2',
 'appdirs==1.4.4',
 'attrs==22.1.0',
 'black>=22.6.0,<23.0.0',
 'boto3==1.24.59',
 'botocore==1.27.59',
 'certifi==2022.12.7',
 'cfgv==3.2.0',
 'coverage==5.4',
 'distlib==0.3.1',
 'filelock==3.0.12',
 'flake8>=4.0.1,<5.0.0',
 'identify==1.5.13',
 'iniconfig==1.1.1',
 'isort>=5.10.1,<6.0.0',
 'joblib==1.2.0',
 'mccabe==0.6.1',
 'mlflow==1.29.0',
 'mock>=4.0.3,<5.0.0',
 'moto>=3.1.5,<4.0.0',
 'mypy-extensions==0.4.3',
 'nodeenv==1.5.0',
 'numpy>=1.22.4,<2.0.0',
 'packaging>=21.3,<22.0',
 'pandas==1.4.2',
 'pluggy==1.0.0',
 'polling==0.3.2',
 'pre-commit==2.10.0',
 'py==1.10.0',
 'pyarrow==7.0.0',
 'pyathena>=2.13.0,<3.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pyparsing==2.4.7',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest-custom-exit-code==0.3.0',
 'pytest>=7.1.1,<8.0.0',
 'regex==2021.8.3',
 'requests==2.28.2',
 'responses==0.23.1',
 's3fs>=2023.3.0,<2024.0.0',
 'six==1.15.0',
 'toml==0.10.2',
 'typed-ast>=1.5.3,<2.0.0',
 'typing-extensions>=4.2.0,<5.0.0',
 'virtualenv==20.4.2']

setup_kwargs = {
    'name': 'hip-data-ml-utils',
    'version': '0.3.7',
    'description': 'Common Python tools and utilities for Hipages ML work',
    'long_description': '# data-ml-utils\nA utility python package that covers the common libraries we use.\n\n## Installation\nThis is an open source library hosted on pypi. Run the following command to install the library\n```\npip install data-ml-utils --upgrade\n```\n\n## Documentation\nHead over to https://data-ml-utils.readthedocs.io/en/latest/index.html# to read our library documentation\n\n## Feature\n### Pyathena client initialisation\nAlmost one liner\n```python\nimport os\nfrom data_ml_utils.pyathena_client.client import PyAthenaClient\n\nos.environ["AWS_ACCESS_KEY_ID"] = "xxx"\nos.environ["AWS_SECRET_ACCESS_KEY"] = "xxx" # pragma: allowlist secret\n\npyathena_client = PyAthenaClient()\n```\n![Pyathena client initialisation](docs/_static/initialise_pyathena_client.png)\n\n### Pyathena query\nAlmost one liner\n```python\nquery = """\n    SELECT\n        *\n    FROM\n        dev.example_pyathena_client_table\n    LIMIT 10\n"""\n\ndf_raw = pyathena_client.query_as_pandas(final_query=query)\n```\n![Pyathena query](docs/_static/query_pyathena_client.png)\n\n### MLflow utils\nVisit [link](https://data-ml-utils.readthedocs.io/en/latest/index.html#mlflow-utils)\n\n### More to Come\n* You suggest, raise a feature request issue and we will review!\n\n## Tutorials\n### Pyathena\nThere is a jupyter notebook to show how to use the package utility package for `pyathena`: [notebook](tutorials/[TUTO]%20pyathena.ipynb)\n\n### MLflow utils\nThere is a jupyter notebook to show how to use the package utility package for `mlflow_databricks`: [notebook](tutorials/[TUTO]%20mlflow_databricks.ipynb)\n',
    'author': 'Hipages Data Team',
    'author_email': 'datascience@hipagesgroup.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
