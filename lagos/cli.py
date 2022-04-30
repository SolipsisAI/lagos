#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from lagos.core import get_article


@click.command()
@click.option("--title", "-t", required=True, help="The title of the article")
def main(title):
    article = get_article(title)
    print(article)
