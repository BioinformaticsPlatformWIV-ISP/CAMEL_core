import re
from pathlib import Path
import typing

import yaml

from camelcore.app.command import Command
from camelcore.app.errors import SnakemakeExecutionError
from camelcore.app.logger import logger


def generate_config_file(config_data: dict[str, typing.Any], output_dir: Path, output_basename: str = 'config.yml') -> str:
    """
    Generates a configuration file for Snakemake in YAML file format.
    :param config_data: Configuration data
    :param output_dir: Output directory
    :param output_basename: Output basename
    :return: Path to config file
    """
    config_path = output_dir / output_basename
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    with config_path.open('w') as handle:
        yaml.dump(config_data, handle)
    logger.info(f"Configuration file created: {config_path}")
    return str(config_path)


def run_snakemake(
        snakefile: str | Path, config_path: str | Path, targets: list[Path], working_dir: Path, threads: int = 8,
        resources: dict[str, typing.Any] | None = None, slurm_args: dict[str, int] | None = None) -> Command:
    """
    Helper function to run snakemake workflows.
    :param snakefile: Workflow snakefile
    :param config_path: Path to configuration file
    :param targets: Target output files
    :param working_dir: Working directory
    :param threads: Number of threads to use
    :param resources: Dictionary of resources by keyword
    :param slurm_args: Dictionary of slurm arguments
    :return: None
    """
    if not working_dir.exists():
        working_dir.mkdir(parents=True)

    # Construct the base command
    command_parts = [
        'snakemake',
        *[str(x) for x in targets],
        '--snakefile', str(snakefile),
        '--configfile', str(config_path),
        '--cores', str(threads)
    ]

    # Add resources if they are specified
    if resources is not None:
        command_parts.append('--resources')
        for key, value in resources.items():
            command_parts.append(f'{key}={value}')

    # Add slurm submit file and parameters if specified
    if slurm_args is not None:
        command_parts.append(f'--cluster "{slurm_args["cluster"]}"')
        for key, value in slurm_args.items():
            if key != 'cluster':
                command_parts.append(f'--{key} {value}')

    # Create and run command
    command = Command(' '.join(command_parts))
    command.run(working_dir)
    if command.exit_code != 0:
        rule_failed = __get_failed_rule(command.stderr)
        logger.error(f"Failed at rule: {rule_failed if rule_failed is not None else 'n/a'}")
        raise SnakemakeExecutionError(command.stdout, command.stderr, rule_failed)
    return command

def __get_failed_rule(stderr: str) -> str | None:
    """
    Returns the name of the rule that failed during Snakemake execution.
    :return: Name of the failed rule (if available)
    """
    for line in reversed(stderr.splitlines()):
        m = re.match(r'Error in rule (\w+):', line.strip())
        if not m:
            continue
        return m.group(1)
    return None
