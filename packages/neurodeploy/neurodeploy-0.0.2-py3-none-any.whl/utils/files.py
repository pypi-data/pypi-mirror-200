import os
from .query import post


def upload_file(data_in, file_path):
    try:
        response = post(
            data_in["url"],
            data=data_in["fields"],
            headers=None,
            files={"file": open(file_path, "rb")},
        )
    except IOError:
        return {"message": "cant send  model file", "status_code": "500"}
    if response["status_code"] == "200":
        return {"message": "yout file is uploaded", "status_code": "200"}
    else:
        return {"message": "yout file is not uploaded", "status_code": "500"}
