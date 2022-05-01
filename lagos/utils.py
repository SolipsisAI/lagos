# -*- coding: utf-8 -*-
def sanitize_wiki_title(title) -> str:
    return title.lower().replace(" ", "_")
