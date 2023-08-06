"""
[![codecov](https://codecov.io/gh/cariad/slash3/branch/main/graph/badge.svg?token=Vq0w74e8YY)](https://codecov.io/gh/cariad/slash3)

# Introduction

**Slash3** is a Python package for building and navigating Amazon Web Services
S3 URIs.

# What's an S3 URI?

An S3 URI (Uniform Resource Identifier) is a string that identifies a bucket,
and optionally a key, in Amazon Web Services S3.

The pattern for an S3 URI is `s3://BUCKET/KEY`.

For example:

- The bucket named "circus" can be described by the URI `s3://circus/`
- The key prefix for all circus images can be described by the URI
`s3://circus/images/`
- The path to Steve's staff photograph can be described by the URI
`s3://circus/images/steve.jpg`

# Installation

Slash3 requires Python 3.9 or later and can be installed from
[PyPI](https://pypi.org/project/slash3/).

```shell
pip install slash3
```

# Usage

## Construct a URI from a URI

If you've already got a string URI then pass it directly to `S3Uri`:

```python
from slash3 import S3Uri

uri = S3Uri("s3://circus/")

uri.bucket  # circus
uri.key     #

uri = S3Uri("s3://circus/images/clowns.jpg")

uri.bucket  # circus
uri.key     # images/clowns.jpg
```

## Construct a URI from a bucket and key

To construct an S3 URI from a bucket name and an optional key, call
`S3Uri.to_uri`:

```python
from slash3 import S3Uri

uri = S3Uri.to_uri("circus")
# s3://circus/

uri = S3Uri.to_uri("circus", "images/clowns.jpg")
# s3://circus/images/clowns.jpg
```

## Join a key suffix with a "/" delimiter

To join a key suffix with a "/" delimiter -- for example, to join an object's
name to a key prefix -- call `S3Uri.join()` or use the `/` operator:

```python
from slash3 import S3Uri

uri = S3Uri("s3://circus/")

images = uri / "images"
# s3://circus/images

clowns = images / "clowns.jpg"
# s3://circus/images/clowns.jpg
```

Slash3 will automatically normalise away any consecutive "/" delimiters.

## Append a key suffix without a delimiter

To append a key suffix without a delimiter, call `S3Uri.append()` or use the `+`
operator:

```python
from slash3 import S3Uri

staff = S3Uri("s3://circus/staff-")

steve = staff + "steve.jpg"
# s3://circus/staff-steve.jpg

penny = staff + "penny.jpg"
# s3://circus/staff-penny.jpg
```

## Get the parent key prefix

To get a URI's parent key prefix, call `S3Uri.parent`:

```python
from slash3 import S3Uri

steve = S3Uri("s3://circus/images/steve.jpg")

steve.parent
# s3://circus/images/
```

## Get a relative key path

To discover the relative path between a specific URI and a parent URI, call
`S3Uri.relative_to`:

```python
from slash3 import S3Uri

avatar = S3Uri("s3://circus/images/staff/steve.jpg")
images = "s3://circus/images/"

avatar.relative_to(images)
# staff/steve.jpg
```

# Support

Please submit all your questions, feature requests and bug reports at
[github.com/cariad/slash3/issues](https://github.com/cariad/slash3/issues). Thank you!

# Licence

Slash3 is [open-source](https://github.com/cariad/slash3) and released under the
[MIT License](https://github.com/cariad/slash3/blob/main/LICENSE).

You don't have to give attribution in your project, but -- as a freelance
developer with rent to pay -- I appreciate it!

# Author

Hello! 👋 I'm **Cariad Eccleston**, and I'm a freelance Amazon Web Services
architect, DevOps evangelist, CI/CD pipeline engineer and backend developer.

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
