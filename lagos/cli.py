#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option("--model", "-m", default=None)
@click.option("--connect", "-c", default="ws://localhost:8001")
def start(model, connect):
    """Start chatbot"""
    from lagos.client import bot

    asyncio.run(bot("conversational", connect_url=connect, model=model))


@cli.command()
@click.option("--host", "-H", default="localhost", help="host")
@click.option("--port", "-P", default=8001, help="port")
def serve(host, port):
    """Start websocket"""
    from lagos.server import app

    asyncio.run(app(host, port))


@cli.command()
@click.option("--model", "-m", default="microsoft/DialoGPT-large")
@click.option("--tokenizer", "-t", default="microsoft/DialoGPT-large")
def app(model, tokenizer):
    """Launch text-based UI"""
    from lagos.tui import Chat

    Chat.run(title="Solipsis", log="textual.log", model=model, tokenizer=tokenizer)
