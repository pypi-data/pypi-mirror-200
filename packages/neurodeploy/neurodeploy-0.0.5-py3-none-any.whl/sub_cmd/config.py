#!/usr/bin/python
from typing import Optional
import typer

import process.nd_config as config
import process.nd_credentials as nd_credentials
import neurodeploy


config_app = typer.Typer()


@config_app.callback()
def config_callback():
    print("Save cli config")


@config_app.command()
def update(
    username: str = typer.Option(
        ..., prompt="Enter your username", help="user username created with ui"
    ),
    password: str = typer.Option(
        ...,
        prompt="Enter your password",
        help="user password created with ui",
        confirmation_prompt=True,
        hide_input=False,
    ),
):
    config.save_config(username)
    neurodeploy.user.login(username, password)
    resp = neurodeploy.credentials.create(username, "credential_of_" + username)
    nd_credentials.save_credentials(resp)
    print("[bold red]Your confguration saved[/bold red]")
    print("[green]To start use : cli --help[/green] ")
