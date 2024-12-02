"""
## Supported types

The following are all type-casting methods of `DotEnv`:

- `env.str`
- `env.bool`
- `env.int`
- `env.float`
- `env.decimal`
- `env.list` (accepts optional `subcast` and `delimiter` keyword arguments)
- `env.json` (casts to a [`JSON object`](https://docs.python.org/3/library/json.html)))
- `env.datetime` (uses fromisoformat() method)
- `env.date` (uses fromisoformat() method)
- `env.time` (uses fromisoformat() method)
- `env.timedelta` (assumes value is an int\float in seconds)
- `env.timestamp` (assumes value is an int\float in seconds)
- `env.url` (recommended to specify the scheme)
- `env.uuid` (assumes value is string of 36 char or 32 without dash; casts to a [`UUID object`](https://docs.python.org/3/library/uuid.html))
- `env.path` (casts to a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html))

- `env.dict` (not implemented yet; accepts optional `subcast_keys`, `subcast_values` and `delimiter` keyword arguments)
- `env.enum` (not implemented yet; casts to any given enum type specified in `type` keyword argument, accepts optional `ignore_case` keyword argument)
- `env.log_level` (will not be implemented, use string)

"""

import os
import sys
import urllib
from typing import IO, Any, Optional, Union

from dotenv import *
from dotenv.main import *

__version__ = "0.1.5"
__vendor__ = "python.dotenv.typecast.onefile"


def read_dotenv(
    dotenv_path: Optional[StrPath] = None,
    stream: Optional[IO[str]] = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
    encoding: Optional[str] = "utf-8",
) -> DotEnv:
    """Parse a .env file and return its content as the DotEnv object.

    The returned dict will have `None` values for keys without values in the .env file.
    For example, `foo=bar` results in `{"foo": "bar"}` whereas `foo` alone results in
    `{"foo": None}`

    Parameters:
        dotenv_path: Absolute or relative path to the `.env` file.
        stream: `StringIO` object with .env's content, used if `dotenv_path` is `None`.
        verbose: Whether to output a warning if the `.env` file is missing.
        override: Whether to override the system environment variables with the variables
            from the `.env` file.
        encoding: Encoding to be used to read the file, default `utf-8`.

    Returns:
        object: DotEnv()

    If both `dotenv_path` and `stream` are `None`, `find_dotenv()` is used to find the
    .env file.
    """

    if dotenv_path is None and stream is None:
        dotenv_path = find_dotenv()

    dotenv = DotEnv(
        dotenv_path=dotenv_path,
        stream=stream,
        verbose=verbose,
        interpolate=interpolate,
        override=override,
        encoding=encoding,
    )
    dotenv.set_as_environment_variables()
    return dotenv


def from_string(text=Union[str, list, dict]) -> io.StringIO:
    if isinstance(text, dict):
        text = "\n".join(text.values())
    if isinstance(text, list):
        text = "\n".join(text)
    if not isinstance(text, str):
        raise ValueError("incorrect `text` type")

    return io.StringIO(text)


def from_string_values(text=Union[str, list, dict]) -> dict:
    return dotenv_values(stream=from_string(text))


def getenv(key: str, default: Any = None) -> Any:
    return os.getenv(key, default)


def _cast(
    self,
    value: Any,
    typecast: Optional[Union[str, type, None]] = Ellipsis,
    *args,
    **kwargs,
) -> Any:
    """ """

    if typecast is Ellipsis:
        return value

    # if typecast in (None, type(None)):  # NoneType:
    #    return None

    if not isinstance(typecast, str):
        raise NotImplementedError("Not implemented yet")

    typecast = typecast.lower()
    val_lo = str(value).lower()
    globals_builtins = globals()["__builtins__"]

    if "bool" == typecast:
        return False if val_lo in ("", "0", "false", "no", "none", False) else True
    elif "path" == typecast:
        return pathlib.Path(value)
    elif "timedelta" == typecast:
        return datetime.timedelta(seconds=float(value))
    elif "timestamp" == typecast:
        return datetime.datetime.fromtimestamp(float(value))
    elif "datetime" == typecast:
        return datetime.datetime.fromisoformat(value)
    elif "date" == typecast:
        return datetime.date.fromisoformat(value)
    elif "time" == typecast:
        return datetime.time.fromisoformat(value)
    elif "json" == typecast:
        return json.loads(value)
    elif "list" == typecast:
        delimiter = kwargs.get("delimiter", ",")
        subcast = kwargs.get("subcast", None)
        a = map(str.strip, value.split(delimiter))
        if subcast:
            if isinstance(subcast, str) and subcast in globals_builtins:
                subcast = globals_builtins[subcast]
            elif isinstance(subcast, type):
                pass
            else:
                raise TypeError(f"subcast type `{subcast}` not found")
            a = map(subcast, a)
        return list(a)

    # elif "dict" == typecast:
    #    return (value)

    elif "url" == typecast:
        try:
            url_parts = urllib.parse.urlsplit(value, scheme="https")
            # print(url_parts)
            url = urllib.parse.urlunsplit(
                url_parts._replace(
                    path=urllib.parse.quote_plus(url_parts.path, safe="/"),
                    fragment=urllib.parse.quote_plus(url_parts.fragment, safe="/"),
                )
            )
            return url
        except Exception as exc:
            raise TypeError(f"Typecast `{typecast}` error! " + str(exc))

    elif typecast in globals_builtins:
        return globals_builtins[typecast].__call__(
            value or (0 if "int" == typecast else "")
        )
    else:
        raise TypeError()


def _env(self, key: str, default: Any = None) -> Any:
    return os.getenv(key, default)


def _getattr(self, name: str) -> Any:
    return lambda key, default=None, *args, **kwargs: self.cast(
        value=(self.get(key) or default), typecast=name, *args, **kwargs
    )
    # правильно доработать метод до привычной сигнатуры DotEnv::get(key, default=None)


sys.modules["dotenv"].main.DotEnv.cast = _cast
sys.modules["dotenv"].main.DotEnv.env = sys.modules["dotenv"].main.DotEnv.getenv = _env
sys.modules["dotenv"].main.DotEnv.__getattr__ = _getattr
sys.modules["dotenv"].read_dotenv = read_dotenv
sys.modules["dotenv"].__all__.append("read_dotenv")
sys.modules["dotenv"].__all__.append("getenv")

__all__ = [*sys.modules["dotenv"].__all__, "DotEnv"]
