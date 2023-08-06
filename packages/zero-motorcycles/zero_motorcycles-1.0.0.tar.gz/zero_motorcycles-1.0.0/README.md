# Zero Motorcycles

[![PyPI - Version](https://img.shields.io/pypi/v/zero-motorcycles.svg)](https://pypi.org/project/zero-motorcycles)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zero-motorcycles.svg)](https://pypi.org/project/zero-motorcycles)

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install zero-motorcycles
```

## Usage

```python
from zero_motorcycles import Zero

zero_client = Zero(username="email", password="password")

# Get units
zero_client.get_units()

# Get last transmit data for a specific unit
zero_client.get_last_transmit(123456)

# Get subscription expiration for a specific unit
zero_client.get_expiration_date(123456)
```

## License

`zero-motorcycles` is distributed under the terms of the [BSD 3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) license.
