"""Base class for a DataSource"""


class BaseDataSource:
    def __init__(self, name):
        self.name = name

    def get_text(self, keyword):
        raise NotImplementedError
