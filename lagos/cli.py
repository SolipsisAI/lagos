#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import click

from lagos.server import app
from lagos.client import bot


@click.group()
def cli():
    pass


@cli.command()
@click.argument("pipeline_name")
@click.option("--connect", "-c", default="ws://localhost:8001")
def start(pipeline_name, connect):
    """Start chatbot"""
    asyncio.run(bot(pipeline_name, connect_url=connect))


@cli.command()
@click.option("--host", "-H", default="localhost", help="host")
@click.option("--port", "-P", default=8001, help="port")
def serve(host, port):
    """Start websocket"""
    asyncio.run(app(host, port))
