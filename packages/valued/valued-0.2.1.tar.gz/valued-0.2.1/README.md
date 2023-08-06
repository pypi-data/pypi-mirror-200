[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/7bf4ee4d616049658be2f1a6d12fb5c0)](https://app.codacy.com?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7bf4ee4d616049658be2f1a6d12fb5c0)](https://app.codacy.com?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![CI/CD Workflow](https://github.com/valued-app/valued.py/actions/workflows/ci-cd.yaml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Valued Python Client

A Python client library for sending events to [Valued](https://valued.app).

## Installation

```bash
$ pip install valued
```

## Usage

You can create a `valued.Client` instance and call `action`, `sync` etc directly on the client.

```python
import os
import valued

# Get the token for authentication.
token = os.environ.get("VALUED_TOKEN") # or wherever you store credentials

# Create a client
client = valued.Client(token)

# Record an action
client.action("report.generated", {
  "customer": { "id": 12 },
  "user": { "id": 123 },
  "attributes": { "format": "pdf" }
})

# Sync user data
client.sync_user({
  "id": 123,
  "name": "Josh Kalderimis",
  "email": "josh@valued.app",
  "location": { "country": "NZ", "region": "Wellington" }
})
```

## Contributing

All commits messages should be in the [Angluar commit style](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commit-message-format)

- feat: A new feature.
- fix: A bug fix.
- docs: Documentation changes.
- style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
- refactor: A code change that neither fixes a bug nor adds a feature.
- perf: A code change that improves performance.
- test: Changes to the test framework.
- build: Changes to the build process or tools.
