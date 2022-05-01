# -*- coding: utf-8 -*-
def sanitize_wiki_title(title) -> str:
    return title.strip().rstrip("|").lower().replace(" ", "_")
