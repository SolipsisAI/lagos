# -*- coding: utf-8 -*-
import requests


def get_ip() -> str:
    r = requests.get("http://icanhazip.com")
    if r.status_code >= 300:
        return "Error"
    return r.text

