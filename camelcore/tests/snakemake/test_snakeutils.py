import unittest

from camelcore.app.testsuite import TestSuite
from camelcore.app.utils import snakeutils


class TestSnakeUtils(TestSuite):
    """
    Tests the snakemake utility classes.
    """

    test_snakefile = TestSuite.get_test_file('workflow_test.smk')

    def test_run_snakefile(self) -> None:
        """
        Tests the run snakefile method.
        :return: None
        """
        config_data = {'working_dir': str(self.running_dir)}
        config_path = snakeutils.generate_config_file(config_data, self.running_dir)
        snakeutils.run_snakemake(str(TestSnakeUtils.test_snakefile), config_path, [], self.running_dir)

    def test_run_snakefile_resources(self) -> None:
        """
        Tests the run snakefile method with the resources parameter set.
        :return: None
        """
        config_data = {'working_dir': str(self.running_dir)}
        config_path = snakeutils.generate_config_file(config_data, self.running_dir)
        command = snakeutils.run_snakemake(
            str(TestSnakeUtils.test_snakefile), config_path, [], self.running_dir, resources={'RAM': 2, 'GPU': 4}
        )
        self.assertIn('--resources', command.command, 'Resources parameter not added')
        self.assertIn('RAM', command.command, 'Resource not added')
        self.assertIn('GPU', command.command, 'Resource not added')

    def test_generate_config_file(self) -> None:
        """
        Tests the generate_config_file method.
        :return: None
        """
        test_config = {'key1': 'value1', 'key2': [1, 2]}
        config_path = snakeutils.generate_config_file(test_config, self.running_dir, 'test_config.yml')
        self.assertTrue(self.running_dir.joinpath('test_config.yml').exists())
        with open(config_path) as handle:
            content = handle.read()
            self.assertIn('key1: value1', content)
            self.assertIn('key2:', content)


if __name__ == '__main__':
    unittest.main()
