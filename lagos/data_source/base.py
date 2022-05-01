"""Base class for a DataSource"""


class BaseDataSource:
    def __init__(self, name):
        self.name = name
        self.results = {}

    def query(self, key, update: bool = False):
        key_parts = self.sanitize(key).split("|")
        root_key = key_parts[0]

        if root_key not in self.results or update:
            self.results[root_key] = self.find(root_key)

        return self.by_key(key)

    def find(self, key, exclude, flatten):
        raise NotImplementedError

    def by_key(self, key):
        key_parts = self.sanitize(key).split("|")
        root_key = key_parts[0]

        if len(key_parts) == 1:
            return self.results.get(root_key)

        return self.results.get(root_key, {}).get("|".join(key_parts))

    def sanitize(self, key):
        raise NotImplementedError
