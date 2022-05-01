#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import click

from lagos.server import app


@click.group()
def cli():
    pass


@cli.command()
def server():
    asyncio.run(app())
