from .wikipedia import WikipediaDataSource


def load_data_source(name: str):
    return {"wiki": WikipediaDataSource}.get(name)
