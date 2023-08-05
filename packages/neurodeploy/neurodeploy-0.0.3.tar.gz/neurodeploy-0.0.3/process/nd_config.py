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
