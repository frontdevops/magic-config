from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Self, Final

from dotenv import load_dotenv, dotenv_values


class MagicConfig(dict):
    """
    Singleton configuration class loading settings from .env files and environment variables.
    Supports:
      - ENV_FILE environment variable for custom .env path
      - env_file argument in constructor
      - arbitrary extra kwargs/data passed on instantiation
      - automatic .env loading from current working directory
      - type casting based on magic.config file
      - automatic database URI generation
    """

    _instance: MagicConfig | None = None
    _initialized: bool = False

    # Mapping of type names to (cast function, default value)
    _TYPE_MAP: Final[dict[str, tuple[callable[[str], Any], Any]]] = {
        "int": (int, 0),
        "float": (float, 0.0),
        "bool": (lambda x: x.lower() in ("1", "true", "yes"), False),
        "str": (str, ""),
        "obj": (json.loads, None),
    }

    # Templates for generating database URIs
    _DB_TEMPLATES: Final[dict[str, str]] = {
        "MONGO": "mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin&tls=false",
        "MYSQL": "jdbc:mysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}",
    }

    def __new__(cls, *args, **kwargs) -> Self:
        # Accept arbitrary args/kwargs so that __new__ won't
        # throw TypeError when user passes BASE_DIR or other params.
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
            self,
            data: dict[str, Any] | None = None,
            env_file: str | None = None,
            **kwargs: Any,
    ) -> None:
        # Prevent re-initialization in the singleton
        if self._initialized:
            return
        super().__init__()
        self._initialized = True

        # 1) Merge positional data dict and keyword args
        #    so that Config({'A':1}, B=2, BASE_DIR=...) works.
        merged = {}
        if data:
            merged |= data  # PEP 584 dict union
        if kwargs:
            merged |= kwargs
        # store everything upper-cased
        self |= {key.upper(): value for key, value in merged.items()}

        # 2) Determine which .env file to load:
        #    priority: ENV_FILE env var > env_file arg > default .env in cwd
        effective_env: str | None = os.getenv("ENV_FILE") or env_file

        if effective_env:
            load_dotenv(effective_env)
            raw_env = dotenv_values(effective_env)
        else:
            load_dotenv()
            raw_env = dotenv_values()

        # 3) Load all .env values into the config dict
        if raw_env:
            self |= {key.upper(): value for key, value in raw_env.items() if value is not None}

        # 4) Apply type casting based on magic.config
        cfg_path = Path.cwd() / "magic.config"
        if cfg_path.exists():
            type_map = dotenv_values(cfg_path)
            for key, typ in type_map.items():
                key_up = key.upper()
                raw_val = os.getenv(key_up)
                if raw_val is None:
                    continue
                item = self._TYPE_MAP.get(typ.lower())
                if item is None:
                    continue
                cast_fn, default = item
                try:
                    self[key_up] = cast_fn(raw_val)
                except Exception:
                    self[key_up] = default

    def __getitem__(self, key: str) -> Any:
        key_up = key.upper()

        # 1) Auto-generate database URI if key ends with "_URL"
        if key_up.endswith("_URI"):
            prefix = key_up.removesuffix("_URI")  # PEP 616
            if tpl := self._DB_TEMPLATES.get(prefix):
                try:
                    return tpl.format(**self)
                except KeyError:
                    pass

        # 2) Return stored value if present
        if key_up in super().keys():
            return super().__getitem__(key_up)

        # 3) Fallback to raw environment variable
        return os.getenv(key_up)

    def __getattr__(self, name: str) -> Any:
        # attribute-style access for config keys
        if name.startswith("_"):
            return super().__getattribute__(name)
        return self[name]

    def __delitem__(self, key: str) -> None:
        # delete a key (case-insensitive)
        super().pop(key.upper(), None)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __dir__(self) -> list[str]:
        """
        Expose dictionary keys in dir() so that Flask
        config.from_object() will pick them up.
        """
        return super().__dir__() + list(self.keys())


# Final singleton instance
Config: Final[MagicConfig] = MagicConfig()
