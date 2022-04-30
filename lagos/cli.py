#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from lagos.core import get_page_text 


@click.command()
@click.argument("title")
@click.option("--exclude", "-e", default=None, help="Delimited by |")
def main(title, exclude):
    result = get_page_text(title, exclude)
    print(result)
