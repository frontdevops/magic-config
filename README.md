# Magic Config

A simple library for easy handling of `.env` files and environment-variables configurations.  
Implements a singleton class so that everywhere in your code you get exactly one shared configuration registry.

> **Requires:** Python 3.9+ (we make use of `str.removeprefix`/`removesuffix` from PEP 616 and modern typing features; Python 3.13 is recommended for full support of `Self`, `Final`, `|`-unions, etc.)

The configuration data is loaded in this order of precedence:

1. **Explicit constructor arguments** (positional `data: dict` or any `**kwargs`)  
2. **`ENV_FILE` environment variable** (if set, points to your `.env` file)  
3. **`env_file=` constructor argument** (pass a path when instantiating)  
4. **Default `.env` in the current working directory**  
5. **Raw OS environment variables**  

Built-in support for:

- **Case-insensitive** access (`Config.DEBUG`, `Config.debug`, `Config["Debug"]` all work)  
- **Automatic type casting** via a `magic.config` file in your project root  
- **Automatic MongoDB/MySQL URI generation** from individual host/user/password vars  
- **Flask integration** via `app.config.from_mapping(Config)` or `app.config.from_object(Config)` (with a `__dir__` override)

---

## Installation

```bash
pip install magic-config
```
## Upgrade
```
pip install --upgrade magic-config
```

PyPI URL: https://pypi.org/project/magic-config/

## Quickstart
### 1. Simple usage
```bash
DEBUG=1 python myapp.py
```

```python
from magic_config import Config

if Config.DEBUG:
    print("Debug mode is ON")
```

You can also do:
```python
if Config.debug:
    ...
if Config["DeBuG"]:
    ...
```

### 2. Custom variables on the fly
You can pass your own values when you first import/instantiate:
```python
from magic_config import MagicConfig, Config
from pathlib import Path

# Positional dict + kwargs
MagicConfig(
    {"NUMBER": 456},
    Boolean=True,
    BASE_DIR=Path(__file__).resolve().parent
)

# Or only kwargs
MagicConfig(
    BASE_DIR=Path(__file__).resolve().parent
)

# Afterwards you can read:
print(Config.BASE_DIR)   # e.g. /www/sites/newhr.org/data/server
print(Config.NUMBER)     # 456
print(Config.BOOLEAN)    # True
```

### 3. Override .env file with ENV_FILE
Instead of relying on the default .env lookup, simply set ENV_FILE in your shell:
```bash
ENV_FILE=dev-1.env python app.py
```

The library will load variables from dev-1.env (instead of .env in CWD).

### 4. Automatic DB-URI generation
In your .env:
```ini
MONGO_HOST=127.0.0.1
MONGO_USER=user
MONGO_PWD=secret
MONGO_DB=test
MONGO_PORT=27017
```

```python
from magic_config import Config

print(Config.MONGO_URI)
# => "mongodb://user:secret@127.0.0.1:27017/test?authSource=admin&tls=false"
```

Likewise for MYSQL_HOST, MYSQL_USER, etc. — just call Config.MYSQL_URI.

### 5. Type casting via magic.config
Create magic.config in your project root:
```ini
DEBUG="bool"
MAX_USERS="int"
FEATURE_FLAGS="obj"
```

```bash
DEBUG=1 MAX_USERS=42 FEATURE_FLAGS='{"beta":true}' python server.py
```

```python
from magic_config import Config

assert isinstance(Config.DEBUG, bool)            # True
assert isinstance(Config.MAX_USERS, int)         # 42
assert isinstance(Config.FEATURE_FLAGS, dict)    # {"beta": True}
```

### 6. Flask integration
By default Flask’s app.config.from_object() only picks up actual attributes listed in dir(obj).
We provide a small `__dir__` override in MagicConfig so you can do:
```python
from flask import Flask
from magic_config import Config

app = Flask(__name__)
app.config.from_object(Config)
```

All your uppercase keys will be imported.
Alternatively, you can treat Config as a plain mapping:
```python
app.config.from_mapping(Config)
# or
app.config.update(Config)
```

Enjoy a cleaner, more powerful way to manage your application configuration!
