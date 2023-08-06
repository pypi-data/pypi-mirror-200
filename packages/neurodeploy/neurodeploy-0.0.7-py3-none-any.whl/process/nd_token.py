#!/usr/bin/python
import os
import ast
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(".").absolute()))


def save_token(resp, dire=".nd", name="token"):
    if "Error" not in resp:
        path = str(Path.home()) + "/" + dire
        if not os.path.exists(path):
            os.makedirs(path)

        f = open(path + "/" + name, "w")
        f.write(str(resp))
        f.close()
        return "ok"


def read_saved_token_date(dire=".nd", name="token"):
    path = str(Path.home()) + "/" + dire

    f = open(path + "/" + name, "r")
    data = f.read()
    f.close()
    resp = ast.literal_eval(data)["expiration"]
    return resp


def check_token_expiry(dire=".nd", name="token"):
    date_token_str = read_saved_token_date(dire, name)
    date_token = datetime.strptime(date_token_str, "%Y-%m-%dT%H:%M:%S.%f")
    current_date = datetime.utcnow()
    if date_token <= current_date:
        resp = 0  # token_expired
    elif date_token > current_date:
        resp = 1  # token_not_expired

    return resp


def read_saved_token(dire=".nd", name="token"):
    path = str(Path.home()) + "/" + dire
    f = open(path + "/" + name, "r")
    data = f.read()
    f.close()
    resp = ast.literal_eval(data)["token"]
    return resp


def token_headers():
    token = read_saved_token()
    headers = {}
    headers["Authorization"] = "Bearer " + str(token)
    return headers
