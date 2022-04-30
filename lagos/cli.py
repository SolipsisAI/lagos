#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from lagos.core import get_page_text


@click.command()
@click.argument("title")
@click.option("--exclude", "-e", default=None, help="Delimited by |")
@click.option("--flatten/--no-flatten", "-f", default=False)
def main(title, exclude, flatten):
    result = get_page_text(title, flatten, exclude)
    print(result)
