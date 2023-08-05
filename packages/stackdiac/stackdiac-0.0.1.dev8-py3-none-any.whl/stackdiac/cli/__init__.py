
import click
import coloredlogs, logging
import os, sys
import yaml

from stackdiac.stackd import sd

logger = logging.getLogger(__name__)

coloredlogs.install(level='DEBUG')

@click.command()
def run():
    click.echo("stackd is workin")

@click.command()
def run_all():
    click.echo("stackd is workin")


@click.command()
@click.option("-p", "--path", default=".", show_default=True, help="project directory")
@click.option("-B", "--no-binaries", is_flag=True, help="do not download binaries")
def update(path, no_binaries:bool, **kwargs):
    sd.root = path
    sd.configure()
    if not no_binaries:
        sd.download_binaries()
    sd.update()


    

@click.group()
def cli():
    pass


from .create import create
from .build import build
from .ui import ui

cli.add_command(create)
cli.add_command(build)
cli.add_command(update)
cli.add_command(ui)

TERRAGRUNT_COMMANDS = [
    "apply", "init", "plan", "destroy", "run-all", "output"
]

def get_cmd(tg_cmd):
    @click.command(context_settings={"ignore_unknown_options": True}, name=tg_cmd)
    @click.option("-p", "--path", default=".", show_default=True, help="project directory")
    @click.option("-b", "--build", is_flag=True, help="build before running terragrunt command")
    @click.argument("target")
    @click.argument("terragrunt_options", nargs=-1)
    def _cmd(path, target, terragrunt_options, build:bool, **kwargs):
        sd.configure()
        if build:
            sd.build()
        sd.terragrunt(target, [tg_cmd, *terragrunt_options], **kwargs)
    return _cmd

for tg_cmd in TERRAGRUNT_COMMANDS:
    cli.add_command(get_cmd(tg_cmd))


