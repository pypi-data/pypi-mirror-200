import sys
import os
import json
from pathlib import Path

sys.path.append(str(Path(".").absolute()))


from utils import query
from utils import files

from process import nd_config
from process import nd_credentials
from process.nd_token import token_headers


def push(name, file="None", lib="tensorflow", filetype="h5"):
    """create a model and upload model file or update modelmeta data.

    :params: name
    :type:   str
    :params: filepath
    :type:   str
    :params: type
    :type:   str
    :params: persistance_type
    :type:   str
    :returns: ok.
    :rtype: dict
    :raises: none

    >>> from neurodeploy import model
    >>> model.push(name, file, lib, filetype)
    """
    conf = nd_config.read_saved_config()
    main_url = conf["url"]
    url = main_url + "/" + "ml-models/" + name
    params = {}
    params["lib"] = lib
    params["filetype"] = filetype
    headers = nd_credentials.credentials_headers()
    headers.update(token_headers())

    response_data = query.put(url, headers, params)
    if "status_code" in response_data:
        if response_data["status_code"] == 400:
            return response_data
    if file != "None":
        resp = files.upload_file(response_data, file)
        return resp
    return {"message": "your model params updated ", "status_code": "200"}


def deploy(name, model, lib="tensorflow"):
    if lib == "tensorflow":
        file_path = "/tmp/model.h5"
        model.save(file_path)
        resp = push(name, file=file_path, lib="tensorflow", filetype="h5")
        os.remove(file_path)
    return resp


def delete(name):
    """delete the model with the given model name for the user associated with the credentials/jwt token..

    :params: name
    :type:   str
    :returns: ok.
    :rtype: dict
    :raises: none

    >>> from neurodeploy import model
    >>> model.delete(name)
    """
    conf = nd_config.read_saved_config()
    main_url = conf["url"]

    url = main_url + "/ml-models" + "/" + name
    headers = nd_credentials.credentials_headers()
    headers.update(token_headers())

    response_data = query.delete(url, headers)
    print(response_data["message"])
    return {"message": response_data["message"], "status_code": "200"}


def list():
    """list models  for logged user.

    :params: none
    :type:   str
    :returns: ok.
    :rtype: dict
    :raises: none

    >>> from neurodeploy import model
    >>> model.list()
    """
    conf = nd_config.read_saved_config()
    main_url = conf["url"]

    url = main_url + "/ml-models"
    headers = nd_credentials.credentials_headers()
    headers.update(token_headers())

    response_data = query.get(url, headers)
    return response_data


def get(name):
    """get metadata (and download link) for model with the given model name for the user associated with the credentials/jwt token.

    :params: name
    :type:   str
    :returns: ok.
    :rtype: dict
    :raises: none

    >>> from neurodeploy import model
    >>> model.list()
    """
    conf = nd_config.read_saved_config()
    main_url = conf["url"]

    url = main_url + "/ml-models" + "/" + name
    headers = nd_credentials.credentials_headers()
    headers.update(token_headers())

    response_data = query.get(url, headers)
    return response_data


def predict(name, data):
    """delete model name for logged user.

    :params: model
    :type:   str
    :params: data
    :type:   list[list]
    :returns: ok.
    :rtype: dict
    :raises: none

    >>> from neurodeploy import model
    >>> model.predict(name,data)
    """
    access = nd_config.read_saved_config()
    user_name = access["username"]
    conf = nd_config.read_saved_config()
    main_url = conf["url_api"]
    url = main_url + "/" + user_name + "/" + name
    headers = nd_credentials.credentials_headers()
    headers.update(token_headers())
    j = {}
    j["payload"] = data
    response_data = query.post(url, json.dumps(j), headers)
    return response_data
