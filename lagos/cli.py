#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from lagos.pipelines import QuestionAnswering


@click.command()
@click.argument("title")
@click.option("--question", "-q")
@click.option("--exclude", "-e", default=None, help="Delimited by |")
def main(title, question, exclude):
    qa_model = QuestionAnswering()
    qa_model.add_context(title, exclude=exclude)
    answer = qa_model.predict(question=question, keyword=title)
    print(answer)
