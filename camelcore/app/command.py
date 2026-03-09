import os
import subprocess
import warnings
from pathlib import Path
from typing import Any
from camelcore.app.logger import logger


class Command:
    """
    Helper class to run commands.
    """

    def __init__(self, command: str | list[str] = None, stdout_path: Path | None = None) -> None:
        """
        Initializes the command object.
        Note it is strongly recommended to initialize commands as a list of string for security
        :param command: (optional) Command line call or list of arguments
        :param stdout_path: stdout path
        :return: None
        """
        self._stdout = None
        self._stderr = None
        self._procedure = None
        self._return_code = None
        self._command = command
        self._stdout_path = stdout_path

    @property
    def stderr(self) -> str:
        """
        Returns the stderr from the command execution.
        :return: Standard error
        """
        return self._stderr

    @property
    def stdout(self) -> str:
        """
        Returns the stdout from the command execution.
        :return: Standard error
        """
        return self._stdout

    @property
    def exit_code(self) -> int:
        """
        Returns the exit code from the command execution.
        """
        return self._return_code

    @property
    def command(self) -> str | list[str]:
        """
        Returns the command line call.
        :return: Command line call
        """
        return self._command

    @command.setter
    def command(self, cmd: str) -> None:
        """
        Sets the command line call.
        :param cmd: Command
        :return: None
        """
        self._command = cmd

    def run(self, folder: Path, stderr_handle=subprocess.PIPE, disable_logging: bool = False, prefix: str | None = None,
            env: dict[str, Any] | None = None) -> None:
        """
        Runs the command given at command initialization
        :param folder: Folder where the command is executed
        :param stderr_handle: Handle for the standard error (e.g. PIPE or STDOUT)
        :param disable_logging: If True, logging is disabled
        :param prefix: If given, this prefix will be added to the commands
        :param env: Environment variables to be set for the command
        :return: None
        """
        if self.command is None:
            raise ValueError("Invalid command 'None'")
        is_shell = isinstance(self._command, str)

        # Add the prefix
        command = self._command
        if prefix:
            if is_shell:
                command = f"{prefix}{self._command}"
            else:
                logger.info('Prefix is not supported when providing command as a list')

        # Log the execution
        if disable_logging is False:
            logger.info(
                f"Executing command: {' '.join(self.command) if isinstance(self.command, list) else self.command}"
            )

        # Output file
        stdout_handle = (self._stdout_path.open('w', encoding='utf-8') if self._stdout_path else subprocess.PIPE)

        try:
            self._procedure = subprocess.run(
                command,
                stdout=stdout_handle,
                stderr=stderr_handle,
                shell=is_shell,
                env={**os.environ, **env} if env is not None else None,
                cwd=folder,
                text=True,
            )
            self._stdout = self._procedure.stdout or ''
            self._stderr = self._procedure.stderr or ''
            self._return_code = self._procedure.returncode
        except FileNotFoundError as err:
            self._stdout = ''
            self._stderr = str(err)
            self._return_code = 1
        finally:
            if stdout_handle is not subprocess.PIPE:
                stdout_handle.close()
        if disable_logging is False:
            logger.debug(f'stdout: {self._stdout}')
            logger.debug(f'stderr: {self._stderr}')

    def run_command(self, folder: Path, stderr_handle=subprocess.PIPE) -> None:
        """
        Runs the command given at command initialization
        :param folder: Folder where the command is executed
        :param stderr_handle: Handle for the standard error (e.g. PIPE or STDOUT)
        :return: None
        """
        warnings.warn(
            'The run_command method is deprecated, please use the run() method instead.', DeprecationWarning)
        self.run(folder, stderr_handle)
