from __future__ import annotations

from types import MethodType
from typing import List, Optional

import click
import typer
from click import Context, MultiCommand, Command
from typer import Typer
from typer.core import TyperGroup

from .commands.config import config
from .commands.create import create
from .commands.delete import delete
from .commands.download import download
from .commands.list import list_command
from .commands.login import login
from .commands.logout import logout
from .commands.trigger import trigger
from .commands.update import update_command
from .commands.upload import upload
from .services import versions
from .services.output import sprint
from .services.versions import (
    print_message_if_devkit_needs_update,
)
from .. import __version__
from ..cli.services import output


def version_cb(value: bool):
    if not value:
        return
    sprint(f"Patterns Devkit CLI version [code]{__version__}")

    print_message_if_devkit_needs_update()

    raise typer.Exit()


def cb(
    stacktrace: bool = typer.Option(False, hidden=True),
    _: bool = typer.Option(
        False,
        "--version",
        help="Print version information and exit.",
        callback=version_cb,
        is_eager=True,
    ),
    disable_version_check: bool = typer.Option(
        False,
        "--disable-version-check",
        help="Don't periodically check if a new devkit version is available for download",
    ),
):
    if stacktrace:
        output.DEBUG = True
    if disable_version_check:
        versions.DISABLE_VERSION_CHECK = True


def result_cb(*_, **__):
    print_message_if_devkit_needs_update()


app = Typer(
    name="patterns",
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="rich",
    callback=cb,
    result_callback=result_cb,
    help=f"""[cyan]Patterns Devkit {__version__}

[not dim][green]Read the docs:[/] https://www.patterns.app/docs/devkit
""",
)

for command in (
    config,
    create,
    delete,
    list_command,
    update_command,
    login,
    logout,
    trigger,
    upload,
    download,
):
    if isinstance(command, typer.Typer):
        command._add_completion = False
        app.add_typer(command)
    else:
        app.command()(command)


def main():
    def _get_group(*args, **kwargs) -> click.Command:
        group = _old_typer_get_group(*args, **kwargs)

        def _list_commands(self, ctx: Context) -> List[str]:
            l = super(TyperGroup, self).list_commands(ctx)
            for c in l:
                sub = super(TyperGroup, self).get_command(ctx, c)
                if isinstance(sub, MultiCommand):
                    l.extend(f"{c} {s}" for s in sub.list_commands(ctx))
            return l

        def _get_command(self, ctx: Context, cmd_name: str) -> Optional[Command]:
            parts = cmd_name.split()
            base = super(TyperGroup, self).get_command(ctx, parts[0])
            if len(parts) == 1:
                return base
            assert len(parts) == 2
            assert isinstance(base, MultiCommand)
            cmd = base.get_command(ctx, parts[1])
            cmd.name = cmd_name
            return cmd

        def format_help(
            self, ctx: click.Context, formatter: click.HelpFormatter
        ) -> None:
            old_list = self.list_commands
            old_get = self.get_command

            self.list_commands = MethodType(_list_commands, self)
            self.get_command = MethodType(_get_command, self)

            typer.core.rich_utils.rich_format_help(
                obj=self,
                ctx=ctx,
                markup_mode=self.rich_markup_mode,
            )

            self.list_commands = old_list
            self.get_command = old_get

        group.format_help = MethodType(format_help, group)

        return group

    _old_typer_get_group = typer.main.get_group
    typer.main.get_group = _get_group
    app()
    typer.main.get_group = _old_typer_get_group
