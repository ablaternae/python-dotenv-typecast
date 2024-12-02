# python dotenv typecast plugin

[![Hits](https://hits.sh/github.com/ablaternae/python-dotenv-typecast.svg)](https://hits.sh/github.com/ablaternae/python-dotenv-typecast/)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ablaternae/python-dotenv-typecast)
[![Code style: black](https://img.shields.io/badge/code%20style-black-ccc.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-green.svg)](https://opensource.org/licenses/BSD-3-Clause)

-----

## TLDR
```console
pip install --upgrade git+https://github.com/ablaternae/python-dotenv-typecast
```
```python
from dotenv_typecast import read_dotenv

env = read_dotenv()

my_string = env.str("ENV_STR")
```

## how it work

This plugin extends the [`dotenv`](https://github.com/theskumar/python-dotenv) library with methods `read_dotenv()`, `DotEnv.cast()`, `DotEnv.getenv()`, `DotEnv.__getattr__()`. 
It works almost like [`environs`](https://github.com/sloria/environs) but without `marshmallow`'s 350kb and valitadion, type cast only.

### plugin initialization
```python
import dotenv_typecast
```
you can import all functions from either `dotenv` or `dotenv_typecast`:
```python
import dotenv_typecast
from dotenv import dotenv_values, load_dotenv, read_dotenv
```
equivalent
```python
from dotenv_typecast import dotenv_values, load_dotenv, read_dotenv
```

### read_dotenv()
the `read_dotenv` signature is similar of other funcs, but __returns instance__ of `dotenv.main.DotEnv`
```python
def read_dotenv(
    dotenv_path: Optional[StrPath] = None,
    stream: Optional[IO[str]] = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
    encoding: Optional[str] = "utf-8",
) -> DotEnv:
```
example:
```python
env = read_dotenv(".env", override=True)

data_dir = env.path("DATA_DIR", default="my_data_dir")
```

## Update
#### 24-12-01
- added method `DotEvn.env(key, default)` (syn `DotEvn.getenv()`) for getting data from environment variables, like a `os.getenv(key, default)`, not from private attribute like origin `DotEvn.get()`
- all type-cast processing goes via its new method 
- so using the parameter `override` seems more logical
- version growed to stable, plugin is ready to production

### type-cast methods
runs  via `DotEnv.__getattr__`

```python
def typecast_method(env_name: str, default_value = None, *args, **kwargs) -> Any
```

#### supported types
The following are all type-casting methods of `DotEnv`:

- `env.str`
- `env.bool`
- `env.int`
- `env.float`
- `env.decimal`
- `env.list` (accepts optional `subcast` and `delimiter` keyword arguments)
- `env.json` (casts to a [`JSON object`](https://docs.python.org/3/library/json.html))
- `env.datetime` (uses fromisoformat() method)
- `env.date` (uses fromisoformat() method)
- `env.time` (uses fromisoformat() method)
- `env.timedelta` (assumes value is an int\float in seconds)
- `env.timestamp` (assumes value is an int\float in seconds)
- `env.url` (recommended to specify the scheme)
- `env.uuid` (assumes value is string of 36 char or 32 without dash; casts to a [`UUID object`](https://docs.python.org/3/library/uuid.html))
- `env.path` (casts to a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html))

#### not implemented
- `env.dict` (not implemented yet; accepts optional `subcast_keys`, `subcast_values` and `delimiter` keyword arguments)
- `env.enum` (not implemented yet; casts to any given enum type specified in `type` keyword argument, accepts optional `ignore_case` keyword argument)
- `env.log_level` (will not be implemented)

