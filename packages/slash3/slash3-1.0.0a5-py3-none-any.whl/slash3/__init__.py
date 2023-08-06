"""
[![codecov](https://codecov.io/gh/cariad/slash3/branch/main/graph/badge.svg?token=Vq0w74e8YY)](https://codecov.io/gh/cariad/slash3)

## Introduction

**Slash3** is a Python package for building and navigating Amazon Web Services
S3 URIs.

## Examples

To construct an S3 URI from its component parts:

```python
from slash3 import S3Uri

S3Uri.to_uri("circus", "images/clowns.jpg")  # s3://circus/images/clowns.jpg
```

To join to a key:

```python
from slash3 import S3Uri

images = S3Uri("s3://circus/") / "images"  # s3://circus/images
clowns = images / "clowns.jpg"  # s3://circus/images/clowns.jpg
```

To append to a key:

```python
from slash3 import S3Uri

staff = S3Uri("s3://circus/") / "staff-"  # s3://circus/staff-
steve = staff + "steve.jpg"  # s3://circus/staff-steve.jpg
penny = staff + "penny.jpg"  # s3://circus/staff-penny.jpg
```

To navigate to a parent path:

```python
from slash3 import S3Uri

steve = S3Uri("s3://circus/images/steve.jpg")
images = steve.parent  # s3://circus/images/
```

To discover a relative path:

```python
from slash3 import S3Uri

steve = S3Uri("s3://circus/images/staff/steve.jpg")
relative = steve.relative_to("s3://circus/images/")  # staff/steve.jpg
```

## Installation

Slash3 requires Python 3.9 or later and can be installed from
[PyPI](https://pypi.org/project/slash3/).

```shell
pip install slash3
```

## Logging

Slash3 respects your root logger configuration. To configure the package's
logger directly, get the logger named "slash3".

## Support

Please submit all your questions, feature requests and bug reports at
[github.com/cariad/slash3/issues](https://github.com/cariad/slash3/issues).
Thank you!

## Licence

Slash3 is [open-source](https://github.com/cariad/slash3) and published under
the [MIT License](https://github.com/cariad/slash3/blob/main/LICENSE).

You don't have to give attribution in your project, but -- as a freelance
developer with rent to pay -- I appreciate it!

## The Author

Hello! 👋 I'm **Cariad Eccleston**, and I'm a freelance Amazon Web Services
architect, DevOps evangelist, CI/CD deployer and backend developer.

You can find me at [cariad.earth](https://cariad.earth),
[github/cariad](https://github.com/cariad),
[linkedin/cariad](https://linkedin.com/in/cariad) and on Mastodon at
[@cariad@tech.lgbt](https://tech.lgbt/@cariad).
"""

from importlib.resources import open_text

from slash3.key import S3Key
from slash3.uri import S3Uri

with open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "S3Key",
    "S3Uri",
]
