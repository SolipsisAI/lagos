#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from lagos.core import ask


@click.command()
@click.argument("title")
@click.option("--question", "-q")
@click.option("--exclude", "-e", default=None, help="Delimited by |")
def main(title, question, exclude):
    ask(title, question=question, exclude=exclude)