#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from lagos.core import get_articles


@click.command()
@click.argument("titles", nargs=-1)
def main(titles):
    print(titles)
    result = get_articles(*titles)
    print(result)
