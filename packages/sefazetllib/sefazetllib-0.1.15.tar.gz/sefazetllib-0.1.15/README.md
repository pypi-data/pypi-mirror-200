# sefazetllib

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

**Documentation**: [https://main.daseasp5gkpi2.amplifyapp.com/](https://main.daseasp5gkpi2.amplifyapp.com/)

**Source code**: [AWS CodeCommit](https://sa-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/jobs-lib-sefaz-ce/browse?region=sa-east-1)

---

**sefazetllib** is a library that provides a simplified and abstracted way to construct ETL/ELT pipelines.

## Features

- Easy to use and understand library for constructing ETL/ELT pipelines.
- Compatibility with popular data processing frameworks, such as [pandas](https://pandas.pydata.org/) and [PySpark](https://spark.apache.org/).
- Support for file formats such as CSV and Parquet.
- Provides the ability to extract, transform and load data with customizable configurations.

## Requirements

**sefazetllib** requires the following to run:

- [Python](https://www.python.org/) 3.7+
- [pandas](https://pandas.pydata.org/) 1.3+
- [PyArrow](https://arrow.apache.org/) 6.0+
- [PySpark](https://spark.apache.org/) 3.0+
- [PyDeequ](https://pydeequ.readthedocs.io/) 1.0+
- [Boto3](https://github.com/boto/boto3) 1.26+

## Installation

First, use [AWS CLI](https://aws.amazon.com/cli/) to get the necessary credentials:

```bash
REGION="sa-east-1"
ACCOUNT_ID="999424586482"
SECRET_NAME="dev/servico-sefaz-ce-9u8PW2"

USERNAME=$(aws secretsmanager get-secret-value --region $REGION --secret-id arn:aws:secretsmanager:$REGION:$ACCOUNT_ID:secret:$SECRET_NAME | grep SecretString | cut -d '\' -f 4 | cut -d '"' -f 2 | cut -d ' ' -f 2)
PASSWORD=$(aws secretsmanager get-secret-value --region $REGION --secret-id arn:aws:secretsmanager:$REGION:$ACCOUNT_ID:secret:$SECRET_NAME | grep SecretString | cut -d '\' -f 8 | cut -d '"' -f 2 | cut -d ' ' -f 2)
```

Then install **sefazetllib** using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install git+https://${USERNAME}:${PASSWORD}@git-codecommit.sa-east-1.amazonaws.com/v1/repos/jobs-lib-sefaz-ce.git
```

## Usage

Here is an example of how to use the **sefazetllib**:

```Python
from typing import Tuple

from pandas import DataFrame

from sefazetllib import Builder
from sefazetllib.etl import ETL
from sefazetllib.extract import ExtractLocal
from sefazetllib.factory.platform import PlatformFactory
from sefazetllib.load import LoadLocal
from sefazetllib.transform import Transform
from sefazetllib.utils.key import SurrogateKey


@Builder
class TestingDataFrame(Transform):
    def execute(self) -> Tuple[str, DataFrame]:
        return (
            "dataframe",
            DataFrame(
                [["tom", 10], ["nick", 15], ["juli", 14]], columns=["Name", "Age"]
            ),
        )


(
    ETL()
    .setPlatform(PlatformFactory("Pandas").create(name="pandas_platform"))
    .transform(TestingDataFrame)
    .load(
        LoadLocal()
        .setFileFormat("parquet")
        .setEntity("load_test")
        .setMode("overwrite")
        .setReference("dataframe")
        .setDuplicates(True)
        .setKey(SurrogateKey().setColumns(["Name", "Age"]).setDistribute(False))
    )
    .extract(
        ExtractLocal()
        .setFileFormat("parquet")
        .setUrl("load_test.parquet")
        .setReference("extract_test")
    )
)
```

## Testing

To run the unit tests, run the following command:

```bash
py -m unittest tests/main.py -v
```

### Status

| Environment      | Status                                                                                                                                                                                                                                                                                                                 |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Feature to Homologation    | ![feature-homologation](https://codebuild.sa-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiYzRJb1JnV2FyS0UxZkVwMk5rNXpCNklFV3BBYVBEMWtLYnMvazVSWDA4WkQvK2twdXMrUmZ5bGRKdUFiU2tEUFF1dkxBRHYrVkdCMDRRNndzV3hKdG13PSIsIml2UGFyYW1ldGVyU3BlYyI6IlFBRmJaZkRpemtwbHVqT0MiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)    |
| Homologation to Production | ![homologation-production](https://codebuild.sa-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiekhWVXpwajRjVjg4TUg2d0RrUy9BOGhNYTFObTZBKzRTMTZscmtaTzdoTmVWTDdaR0xZbjMrOTZVT3ZqTU40eFFEYzJGZkFtUzNSRTl5b2x5ajZOMXlBPSIsIml2UGFyYW1ldGVyU3BlYyI6ImUxajQxOG50TkZkWHh2T2oiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main) |

## License

**sefazetllib** is released under the [Apache-2.0](/LICENSE).
