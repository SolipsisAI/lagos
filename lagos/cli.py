#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import click

from lagos.server import app


@click.group()
def cli():
    pass


@cli.command()
@click.option("--host", "-H", default="localhost", help="host")
@click.option("--port", "-P", default=8001, help="port")
def server(host, port):
    asyncio.run(app(host, port))
