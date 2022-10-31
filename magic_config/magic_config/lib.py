import os
import sys
import builtins
from dotenv import dotenv_values


# @singleton
class MagicConfig(dict):
    """
    MagicConfig magic class :)
    """
    __instance: 'Self' = None
    __data: dict = {}
    __env_file = None

    def set_attr(self, key: str, t: str = "str") -> None:
        """Set attribute to object"""
        key = key.upper()
        cast = getattr(builtins, t)
        self.__data[key] = cast(os.getenv(key))

    def __new__(cls, *args, **kwargs) -> 'Self':
        """Create singleton instance of MagicConfig"""
        if cls.__instance:
            return cls.__instance
        cls.__instance = super(MagicConfig, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, data: dict | None = None, env_file=None) -> None:
        """
        Constructor
        """
        super().__init__()

        if env_file is not None:
            self.__env_file = env_file

        if data is not None:
            for key, val in data.items():
                self.__data[key.upper()] = val

        if self.__env_file is None:
            run_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
            file = f"{run_dir}/.env"

            if not os.path.exists(file):
                run_dir = os.path.dirname(os.path.realpath(__file__))
                file = f"{run_dir}/.env"

            self.__data.update(dict(dotenv_values(file)))
        else:
            self.__data.update(dict(dotenv_values(self.__env_file)))

        list_of_env_vars_file = os.path.realpath(os.path.dirname(os.path.realpath(sys.argv[0])) + "/magic.config")
        if os.path.exists(list_of_env_vars_file):
            for key, val in dotenv_values(list_of_env_vars_file).items():
                self.set_attr(key, val)

    def init(self, **kwargs) -> None:
        """Re init class constructor"""
        self.__data = {}
        self.__init__(**kwargs)

    def __getattr__(self, key: str) -> str | int:
        """Get attribute from config object like"""
        return self.__getitem__(key)

    def dburi_generator(self, key: str) -> str | None:
        """Generate db uri"""
        if "MONGO_URL" == key:
            return (
                f"mongodb://{self.__data['MONGO_USER']}"
                f":{self.__data['MONGO_PWD']}"
                f"@{self.__data['MONGO_HOST']}"
                f":{self.__data['MONGO_PORT']}"
                f"/{self.__data['MONGO_DB']}"
                "?authSource=admin&tls=false"
            )
        elif "MYSQL_URL" == key:
            return (
                f"jdbc:mysql://{self.__data['MYSQL_USER']}"
                f":{self.__data['MYSQL_PWD']}"
                f"@{self.__data['MYSQL_HOST']}"
                f":{self.__data['MYSQL_PORT']}"
                f"/{self.__data['MYSQL_DB']}"
            )
        return None

    def __getitem__(self, key: str):
        """Get item from config list like"""
        key = key.upper()

        if val := self.dburi_generator(key):
            return val

        if val := self.__data.get(key, None):
            return val

        if val := os.getenv(key):
            return val

        return None

    def __delitem__(self, key: str) -> None:
        """Delete item from config list like"""
        self.__delitem__(key)

    def __len__(self) -> int:
        """Get length of config list like"""
        return len(self.__data)

    def __iter__(self) -> iter:
        """Get iterator of config list like"""
        return iter(self.__data)

    def __str__(self) -> str:
        """Get string representation of config list like"""
        return str(self.__data)

    def __repr__(self) -> str:
        """Get representation of config list like"""
        return repr(self.__data)


Config = MagicConfig()
