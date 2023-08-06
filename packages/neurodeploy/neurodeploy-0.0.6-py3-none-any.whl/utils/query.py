#!/usr/bin/python
import requests
import json


def post(url, data, headers=None, files=None, params=None):
    try:
        response = requests.post(
            url, data=data, files=files, headers=headers, params=params
        )
    except requests.exceptions.RequestException as e:
        return {"message": str(e), "status_code": "400"}

    if str(response.status_code) in ["200", "201"]:
        response_data = response.json()
        return response_data
    elif str(response.status_code) in ["204"]:
        return {"message": "post ok", "status_code": "200"}
    else:
        return {"message": response.text, "status_code": response.status_code}


def get(url, headers=None, params=None):
    try:
        response = requests.get(url, headers=headers, params=params)
        if str(response.status_code) in ["200", "201"]:
            response_data = response.json()
            return response_data
        else:
            return {"message": response.text, "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"message": str(e), "status_code": "400"}


def put(url, headers, params=None, data=None):
    try:
        response = requests.put(url, data=data, headers=headers, params=params)
        if str(response.status_code) in ["200", "201"]:
            response_data = response.json()
            return response_data
        else:
            return {"message": response.text, "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"message": str(e), "status_code": "400"}


def delete(url, headers, params=None):
    try:
        response = requests.delete(url, headers=headers, params=params)
        if str(response.status_code) in ["200", "201"]:
            response_data = response.json()
            return response_data
        else:
            return {"message": response.text, "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"message": str(e), "status_code": "400"}
