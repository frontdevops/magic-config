import sys

if sys.version_info < (3, 10):
    raise ImportError('Your Python version {0} is not supported by MagicConfig, please install '
                      'Python 3.10.8+'.format('.'.join(map(str, sys.version_info[:3]))))

from .magic_config import *

__all__ = (
    "MagicConfig",
    "Config"
)

__version__ = '0.0.6'
