import json
import sys
from pathlib import Path

sys.path.append(str(Path(".").absolute()))

from utils import query
from process import nd_credentials
from process import nd_token
from process import nd_config


def login(username, password):
    """login user to get jwt token saved on conf file.

    :params: username
    :type:   str
    :params: password
    :type:   str
    :returns: ok.
    :rtype: dict
    :raises: none

    >>> from neurodeploy import users
    >>> users.login(username, password)
    """
    conf = nd_config.save_config(username)
    conf = nd_config.read_saved_config()
    main_url = conf["url"]
    url = main_url + "/sign-in"
    headers = {}
    headers["username"] = username
    headers["password"] = password
    data = None
    response_data = query.post(url, data, headers)
    resp = nd_token.save_token(response_data)
    return resp
