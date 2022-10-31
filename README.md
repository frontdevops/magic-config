# magic-config
A simple library for easy handling of .env files and environment variables configurations

This library is a class for working with configurations. The class is implemented as a singleton, which allows you to always have exactly one instance of the same data registry everywhere.

The configuration data itself is taken from the .env file or from environment variables.

## Example:
```sh
DEBUG=1 myapp.py
```

My app script:

```py
from magic_config import Config

# You can access to variables as property of class object
if Config.DEBUG:
  ...

# You can access to variables in lower case (and camel case, and other case)
if Config.debug:
  ...

# You can access to variables as key of dict object
if Config["debug"]:
  ...

```

## Configure custom variables
```py
You can add variables to the object

# as dict
MagicConfig({
    "Number": 456,
    "Boolean": True
})

# as named arguments
MagicConfig(
    Number=456,
    Boolean=True
)
```

## Prepared autogenerators for DB URIs
For example in .env  file you can write only this data:
```
MONGO_HOST="127.0.0.1"
MONGO_USER="user"
MONGO_PWD="*****"
MONGO_DB="test"
MONGO_PORT=27017
```

and in code you can call the MONGO_URL

```py
from magic_config import Config

Config.MONGO_URL

# output:
# mongodb://user:passwd@127.0.0.1:27017/test?authSource=admin&tls=false
```

## Set type casting for environment variables

For example if you create in source root magic.config file and write:
```bash
DEBUG="bool"
DEBUG_STEP="bool"
DEBUG_USER_ID="int"
```

then you run 

```bash
DEBUG=1 DEBUG_STEP=1 DEBUG_USER_ID=1 DEBUG_USER_ID=10011888 python server.py
```

```py
Config.DEBUG # True
Config.DEBUG_STEP # True
Config.DEBUG_USER_ID # int(10011888)
```
