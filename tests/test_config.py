import os
import unittest
from magic_config.magic_config import Config, MagicConfig


class TestMagicConfig(unittest.TestCase):
    """

    """

    def setUp(self) -> None:
        """
        Set up test
        :return:
        """
        MagicConfig({
            "Number": 456,
            "Boolean": True
        })
        # env_file = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/../.env")
        # MagicConfig(env_file=env_file)

    def test_singleton_instance(self):
        print("\nRun test_singleton_instance")
        self.assertEqual(Config, MagicConfig())

    def test_magic_config(self):
        self.assertEqual(Config.Number, 456)
        self.assertTrue(Config.Boolean)

    def test_env_loaded(self):
        print("\nRun test_env_loaded")
        self.assertEqual(Config.FOO, "123")
        self.assertEqual(Config.BAR, "Some config string")

    def test_lower_case(self):
        print("\nRun test_lower_case")
        self.assertEqual(Config.foo, "123")
        self.assertEqual(Config.bar, "Some config string")

    def test_dict_access_key(self):
        print("\nRun test_dict_access_key")
        self.assertEqual(Config["foo"], "123")
        self.assertEqual(Config["bar"], "Some config string")

    def test_enviroment_variables_cast_type(self):
        """
        This variable with cast type setted in magic.config file
        DEBUG="bool"
        """
        print("\nRun test_enviroment_variables_cast_type")
        os.environ["DEBUG"] = "1"
        self.assertTrue(Config["DEBUG"])

    def test_enviroment_variables(self):
        """
        Test enviroment variables
        """
        print("\nRun test_enviroment_variables")
        os.environ["DEBUG_MODE"] = "1"
        self.assertEqual(Config["DEBUG_MODE"], "1")


if __name__ == '__main__':
    unittest.main()
