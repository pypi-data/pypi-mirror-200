#!/usr/bin/python
import sys
import os
import ast

import sys
from pathlib import Path

sys.path.append(str(Path(".").absolute()))


from pathlib import Path


def save_credentials(data, dire=".nd", name="credentials"):
    path = str(Path.home()) + "/" + dire
    if not os.path.exists(path):
        os.makedirs(path)
    f = open(path + "/" + name, "w")
    f.write(str(data))
    f.close()
    return "ok"


def read_saved_credentials(dire=".nd", name="credentials"):
    path = str(Path.home()) + "/" + dire
    try:
        f = open(path + "/" + name, "r")
        data = f.read()
        f.close()
        resp = ast.literal_eval(data)
        return resp
    except:
        return {"message": "no credential saved", "status_code": "500"}


def credentials_headers():
    access = read_saved_credentials(dire=".nd", name="credentials")
    headers = {}
    if access["status_code"] != "500":
        headers["access_key"] = access["access_key"]
        headers["secret_key"] = access["secret_key"]
    return headers
