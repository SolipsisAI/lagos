"""Base class for a DataSource"""


class BaseDataSource:
    def __init__(self, name):
        self.name = name
        self.results = {}

    def query(self, key, update: bool = False):
        if key not in self.results or update:
            self.results[key] = self.find(key)
        return self.by_key(key)

    def find(self, key, exclude, flatten):
        raise NotImplementedError

    def by_key(self, key):
        return self.results.get(key)

    def sanitize(self, key):
        raise NotImplementedError
