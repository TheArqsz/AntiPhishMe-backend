<div style="text-align:center; width:20%">
    <img src="Logo.png" alt="AntiPhishMe Logo"/>
</div>

# Phishing add-on backend

Travis status: [![Build Status](https://travis-ci.com/TheArqsz/phishing_backend.svg?branch=develop)](https://travis-ci.com/TheArqsz/phishing_backend)

Code coverage: [![codecov](https://codecov.io/gh/TheArqsz/AntiPhishMe-backend/branch/develop/graph/badge.svg)](https://codecov.io/gh/TheArqsz/AntiPhishMe-backend)

## Prerequisites

- python >3.6
- pip

## Installation

```python3
pip install -r requirements.txt
```

## Run

```python3
python src/app.py
```

## UI

At default, swaggerUI can be found at `localhost:5000/api/v1/ui`

## Environmental variables

| variable's name  | definition  | example  | default value |
|:-:|:-:|:-:|:-:|
| ENV     | Define environment for project  | `DEV`, `DOCKER_DEV`, `PROD`  | `DEV` |  
| DEBUG   | If set, logging level is set to DEBUG and flask's debugger is on  | `True`, `False`  | `False` |
| PORT    | Port on which app will listen   | `5000`  | `5000` |
| HOST    | IP in which app will listen     | `127.0.0.1`, `0.0.0.0`    | `127.0.0.1` |
| DOMAIN  | Domain's name for swagger. API requests use this as target  | `localhost:5000`. `example.com` | Same as `HOST:PORT` | 
| BASE_PATH | Base path for swagger | `/api/v1` | `/api/v1` |
| URLSCAN_API_KEY | API key for urlscan.io | `-` | `-` |
| SAFEBROWSING_API_KEY | API key for safebrowsing | `-` | `-` |
| AUTH_API_KEY | API key for server and db endpoints | `-` | `test_api_key_978675645342312` |
