#!/usr/bin/python
import os
import ast
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(".").absolute()))


from pathlib import Path


def save_config(
    username,
    url="https://user-api.neurodeploy.com",
    dire=".nd",
    name="config",
    url_api="https://api.neurodeploy.com",
):
    path = str(Path.home()) + "/" + dire
    if not os.path.exists(path):
        os.makedirs(path)

    config = {}
    config["username"] = username
    config["url"] = url
    config["url_api"] = url_api
    f = open(path + "/" + name, "w")
    f.write(str(config))
    f.close()

    return "Config saved"


def read_saved_config(dire=".nd", name="config"):
    path = str(Path.home()) + "/" + dire
    f = open(path + "/" + name, "r")
    data = f.read()
    f.close()
    resp = ast.literal_eval(data)
    return resp


def read_env_config():
    env = {}
    env["secret_key"] = os.getenv(
        "ND_SECRET_KEY"
    )  # user acces key value to auth to api
    env["access_key"] = os.getenv(
        "ND_ACCESS_KEY"
    )  # usr secret key value to auth to api
    env["default_lib"] = os.getenv("ND_DEFAULT_LIB")  # Default ml library used
    env["default_filetype"] = os.getenv(
        "ND_DEFAULT_FILETYPE"
    )  # Default ml model file extention
    env["default_confdir"] = os.getenv(
        "ND_DEFAULT_CONFDIR"
    )  # Default cli configuration path to store username / token / credentials
    env["default_endpoint"] = os.getenv(
        "ND_DEFAULT_ENDPOINT"
    )  # Default neurodeploy endpoint domain name
    return env
