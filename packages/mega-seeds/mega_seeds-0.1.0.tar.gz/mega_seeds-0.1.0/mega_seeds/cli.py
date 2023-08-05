import importlib

import asyncclick as click

from .runner import Seed


@click.command()
@click.option(
    "-A", "--app", required=True, type=str, help="The name of the application"
)
@click.option("-m", "--message", type=str, default="")
@click.argument(
    "action", type=click.Choice(["create_file", "execute"]), required=True
)
async def seeds(app: str, action: str, message: str) -> None:
    module, seeds_app = app.split(":")
    runner: Seed = getattr(importlib.import_module(module), seeds_app)
    if action == "create_file":
        await runner.create_file(message)
    elif action == "execute":
        await runner.execute()
