# -*- coding: utf-8 -*-
from datetime import datetime


def sanitize_wiki_title(title) -> str:
    return title.strip().rstrip("|").lower().replace(" ", "_")


def timestamp():
    return datetime.now().strftime("%H:%M:%S")
