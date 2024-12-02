# python dotenv typecast plugin
[in English](./README.en.md)

## Установка и запуск

```console
pip install --upgrade git+https://github.com/ablaternae/python-dotenv-typecast
```
```python
from dotenv_typecast import read_dotenv

env = read_dotenv()

example = env.str("EXAMPLE_STRING")
```

## Подробности

Скрипт расширяет возможности известной библиотеки [`dotenv`](https://github.com/theskumar/python-dotenv) методами приведения типов.
Получается почти как [`environs`](https://github.com/sloria/environs), но не тащит за собой в зависимостях 350кб `marshmallow`.

Инициализация плагина выполняется при импорте
```python
import dotenv_typecast
```
Все функции можно импортировать как из `dotenv`, так и из `dotenv_typecast`
```python
import dotenv_typecast
from dotenv import dotenv_values, load_dotenv, read_dotenv
```
или
```python
from dotenv_typecast import dotenv_values, load_dotenv, read_dotenv
```

После инициализации к модулю `dotenv` будет добавлена функция `read_dotenv`, которая работает аналогично другим функциям, но __возвращает объект__ `DotEnv`
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

```python
env = read_dotenv(".env", override=True)

data_dir = env.path("DATA_DIR", default="my_data_dir")
```

## Обновление
#### 01.12.24
- Добавлен метод `DotEvn.env(key, default)` получения данных не из внутреннего массива (который формируется из файла или строки), а из переменных окружения, как это делает `os.getenv(key, default)` 
- Весь каст теперь идёт через него, а не оригинальный метод `DotEvn.get`
- Таким образом, параметр `override` выглядит более логичным
- Версия повышена до стабильной

## Методы приведения типов
имеют схожую сигнатуру и обрабатываются через `DotEnv.__getattr__`
```python
def typecast_method(env_name: str, default_value = None, *args, **kwargs) -> Any
```
список методов, в целом, аналогичен `environs`:
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

-----
<!-- ![GitHub Repo stars](https://img.shields.io/github/stars/ablaternae/python-dotenv-typecast)
![GitHub watchers](https://img.shields.io/github/watchers/ablaternae/python-dotenv-typecast) -->
[![Hits](https://hits.sh/github.com/ablaternae/python-dotenv-typecast.svg)](https://hits.sh/github.com/ablaternae/python-dotenv-typecast/)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ablaternae/python-dotenv-typecast)
[![Code style: black](https://img.shields.io/badge/code%20style-black-ccc.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-green.svg)](https://opensource.org/licenses/BSD-3-Clause)

