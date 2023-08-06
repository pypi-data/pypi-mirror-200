# Logger

## Purpose
This Logging Manager is to be used as a standardized system and structure to enable logging on different product offerings. We intend the logs to not only enable debugging platform exceptions, but to provide visibility, analytics and reporting on the health, engagement and usage of our products and systems.

## How to use this Package in your Code

### 1. Install pip Package

execute following command to install pip package
```
python -m pip install mh-logger
```

### 2. Import and Use

Following is the sample code to use this package in your code. simply import and start logging.

```
from mh_logger import LoggingManager

logger = LoggingManager("TestLogger")


def test_logging_function():
    logger.info("this is a sample log", json_params={"hello", "world"})


test_logging_function()

```

Sample Stream Log Output:
```
2023-03-16 20:22:36,561 [INFO] - TestLogger: this is a sample log - JSON Payload: {'hello', 'world'}
```

Set following environment variable if you want to push logs to GCP Cloud Logging service while testing locally.

```
SERVICE_ACCOUNT_KEY_PATH=path-to-service-account-key-file\moonhub-search-66f471d68099.json
```

you can exclude unwanted keys from json payload by setting following environment variable. where each list index contains the name of key that needs to be excluded from json payload while logging.

```
EXCLUDE_KEYS=["query", "response"]
```


## Steps to Create and Upload Package
### 1. Create Token (First Time Only)
- Goto `pypi.org` and create your login
- Go to api-tokens and create your API token to securely upload your packages.
- Copy and save your token in a safe place on your disk.

### 2. Install Dependencies (First Time Only)
Install following
```
python -m pip install --upgrade build
python -m pip install --upgrade twine
```

### 3. Build Package

execute following command
```
python -m build
```

Once the process above is completed, a new directory is generated called `dist/` with two files in it. The `.tag.tz` file is the source archive and the `.whl*` file is the built archive. These files represent the distribution archives of our Python package which will be uploaded to the Python Package Index and installed by pip in the following sections.

### 4. Check and Upload Package to PyPi Server
`twine` is a python package that goes through a checklist of items to see if your distribution/package is compatible for publishing.

Check if your distribution is all set to go .

execute following command to check distributions before upload
```
twine check dist/*
```

execute following command to upload latest distribution
```
twine upload --skip-existing --repository-url https://upload.pypi.org/legacy/ dist/*
```
