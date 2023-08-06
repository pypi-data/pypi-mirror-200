#!/usr/bin/env python3

import os
import stat
import sys
from pathlib import Path

import click

RUN_CONFIGS_DIR: str = ".run_configs"


PathNotFoundError = Exception


def get_help_text(run_config: Path) -> str:
    # TODO: stub
    return str(run_config.absolute())


def get_base_dir() -> Path:
    cwd = Path(os.getcwd())
    try:
        rc_path = next(cwd.glob(RUN_CONFIGS_DIR))
        if rc_path.is_dir():
            return cwd
    except StopIteration:
        ...
    for path in cwd.parents:
        try:
            rc_path = next(path.glob(RUN_CONFIGS_DIR))
            if rc_path.is_dir():
                return path
        except StopIteration:
            ...
    raise click.UsageError(
        f"No {RUN_CONFIGS_DIR} found in current path or its parents."
    )


def get_rc_dir(base_dir: Path) -> Path:
    return base_dir / RUN_CONFIGS_DIR


def get_run_configs(base_dir: Path, incomplete: str = "") -> list[Path]:
    return [
        rc
        for rc in filter(
            lambda p: p.name.startswith(incomplete), get_rc_dir(base_dir).glob("**/*")
        )
        if rc.is_file() and os.access(str(rc.absolute()), os.X_OK)
    ]


class RunConfigType(click.ParamType):
    name = "run_config"

    def shell_complete(self, ctx, param, incomplete):
        try:
            base_dir = _get_param(ctx, "base_dir")
        except click.UsageError:
            _, exc_value, _ = sys.exc_info()
            click.echo(f"\n{exc_value}\n", file=sys.stderr)
            return []
        # return [click.shell_completion.CompletionItem(" ", help=exc_value)]
        return [
            click.shell_completion.CompletionItem(
                str(p.relative_to(get_rc_dir(base_dir))), help=get_help_text(p)
            )
            for p in get_run_configs(base_dir, incomplete)
        ]


def _get_param(ctx: click.Context, param: str) -> click.Parameter:
    if param in ctx.params:
        return ctx.params[param]
    if ctx.default_map is not None and param in ctx.default_map:
        return ctx.default_map[param]
    if (default_param := ctx.lookup_default(param)) is not None:
        return default_param
    for p in ctx.command.params:
        if p.name == param:
            return p.get_default(ctx)
    raise Exception(f"Could not find parameter {param}.")


def list(ctx, _, value) -> None:
    if not value or ctx.resilient_parsing:
        return
    base_dir = _get_param(ctx, "base_dir")
    commands = []
    help_texts = []
    for rc in get_run_configs(base_dir):
        commands.append(str(rc.relative_to(get_rc_dir(base_dir))))
        help_texts.append(get_help_text(rc))
    if not commands:
        click.echo("No run configs found.")
        ctx.exit(0)
    longest_command = max(len(c) for c in commands)
    for command, help_text in zip(commands, help_texts):
        click.echo(f"{command.ljust(longest_command)}\t{help_text}")
    ctx.exit(0)


def print_zsh_completion(ctx, _, value) -> None:
    if not value or ctx.resilient_parsing:
        return
    print('eval "$(_RC_COMPLETE=zsh_source rc)"')
    ctx.exit(0)


@click.command()
@click.argument("run_config", type=RunConfigType())
@click.argument("args", nargs=-1)
@click.option(
    "--make-executable",
    is_flag=True,
    help="Make run config executable if it isn't already.",
)
@click.option(
    "--base-dir",
    type=click.Path(exists=True, file_okay=False, readable=True, path_type=Path),
    default=get_base_dir,
    is_eager=True,
    help=(
        "Base directory to run from. Defaults to the first directory containing a .run_configs directory."
        " Should contain a .run_configs directory with executable run configs."
    ),
)
@click.option(
    "--list",
    "list_configs",
    is_flag=True,
    help="List available run configs.",
    callback=list,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--zsh-completion",
    is_flag=True,
    is_eager=True,
    expose_value=True,
    help="Print zsh completion script.",
    callback=print_zsh_completion,
)
@click.version_option()
def cli(
    run_config: str, args: tuple[str], base_dir: Path, make_executable: bool = False
) -> None:
    """Run a run config

    A run config can be any executable file in the .run_configs directory.
    """
    rc_dir = get_rc_dir(base_dir)
    rc = rc_dir / run_config
    if not rc.exists():
        raise click.UsageError(f"Run config {run_config} does not exist in {rc_dir}.")
    if not os.access(str(rc.absolute()), os.X_OK):
        if make_executable or click.confirm(
            "Run config not executable. Change permissions?", abort=True
        ):
            os.chmod(
                str(rc.absolute()), os.stat(str(rc.absolute())).st_mode | stat.S_IEXEC
            )
    os.chdir(base_dir)
    args_list = list(args) if len(args) > 0 else []
    try:
        os.execv(str(rc.absolute()), [str(rc)] + args_list)
    except OSError as e:
        raise click.FileError(rc, f"{e}")


if __name__ == "__main__":
    cli()
