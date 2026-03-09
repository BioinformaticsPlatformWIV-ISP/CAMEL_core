from camelcore.app.command import Command
from camelcore.app.testsuite import TestSuite


class TestCommand(TestSuite):
    """
    Tests for the command object.
    """

    def test_run_command(self) -> None:
        """
        Tests the run command method.
        :return: None
        """
        command = Command(['echo', 'hello'])
        command.run(self.running_dir, disable_logging=False)
        self.assertEqual(command.stdout.strip(), "hello")
        self.assertEqual(command.exit_code, 0)

    def test_run_failing_command(self) -> None:
        """
        Tests a failing command.
        :return: None
        """
        command = Command(['non_existing_command'])
        command.run(self.running_dir)
        self.assertNotEqual(command.exit_code, 0)

    def test_run_with_env_variables(self) -> None:
        """
        Tests passing environment variables to the command.
        :return: None
        """
        command = Command('echo $TEST_VAR')
        command.run(self.running_dir, env={"TEST_VAR": "test_value"})
        self.assertEqual(command.stdout.strip(), "test_value")

    def test_run_redirect(self) -> None:
        """
        Tests running redirecting to a file.
        :return: None
        """
        path_out = self.running_dir / 'output.txt'
        command = Command(['echo', '123'], stdout_path=path_out)
        command.run(self.running_dir)
        with path_out.open() as handle:
            self.assertEqual(handle.read().strip(), "123")

    def test_run_with_prefix(self) -> None:
        """
        Tests running a command with a prefix.
        :return: None
        """
        command = Command("echo 'prefixed'")
        command.run(self.running_dir, prefix="echo 'prefix: '; ")
        self.assertIn("prefix: ", command.stdout)
        self.assertIn("prefixed", command.stdout)
