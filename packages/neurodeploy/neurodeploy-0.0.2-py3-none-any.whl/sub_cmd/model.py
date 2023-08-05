#!/usr/bin/python
from typing import Optional
import typer
import time
from rich import print

from neurodeploy import model

model_app = typer.Typer()


@model_app.callback()
def model_callback():
    print("Running a model command")


@model_app.command("push")
def model_push(
    name: str = typer.Option(..., help="Your model name"),
    file_path: str = typer.Option("None", help="Your model file path on your computer"),
    type: str = typer.Option("tensorflow", help="Your model library"),
    persistance_type: str = typer.Option("h5", help="Your model persistance type"),
):
    """
    #model create update
    """
    resp = model.push(name, file_path, type, persistance_type)
    print(resp)


@model_app.command("delete")
def model_delete(name: str = typer.Option(..., help="Your model name to delete")):
    """
    #model delete
    """
    resp = model.delete(name)
    print(resp)


@model_app.command("get")
def model_get(name: str = typer.Option(..., help="Your model name to get info")):
    """
    #model get
    """
    resp = model.get(name)
    print(resp)


@model_app.command("list")
def models_list():
    """
    #model get
    """
    resp = model.list()
    print(resp)


@model_app.command("predict")
def model_predict(
    name: str = typer.Option(..., help="Your model name"),
    data: str = typer.Option(..., help="Your payload"),
):
    """
    #model predict
    """
    resp = model.predict(name, data)
    print(resp)
