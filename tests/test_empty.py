import os
import unittest
from magic_config.magic_config import Config, MagicConfig


class TestMagicConfig(unittest.TestCase):
    """

    """

    def test_none_var(self):
        self.assertEqual(Config.anyvar, None)


if __name__ == '__main__':
    unittest.main()
