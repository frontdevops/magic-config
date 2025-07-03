# import sys
# if sys.version_info < (3, 13, 0):
#     raise ImportError('Your Python version {0} is not supported by MagicConfig, please install '
#                       'Python 3.13+'.format('.'.join(map(str, sys.version_info[:3]))))

from .lib import MagicConfig, Config

__all__ = (
    "MagicConfig",
    "Config"
)

__version__ = '1.0.0'

