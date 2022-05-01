#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import click

from lagos.server import app


@click.group()
def cli():
    pass


@cli.command()
@click.argument("pipeline_name")
@click.option("--connect", "-c", default="http://localhost:8001")
def start(pipeline_name, connect):
    """Start chatbot"""
    print(pipeline_name, connect)


@cli.command()
@click.option("--host", "-H", default="localhost", help="host")
@click.option("--port", "-P", default=8001, help="port")
def serve(host, port):
    asyncio.run(app(host, port))
