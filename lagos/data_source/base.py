"""Base class for a DataSource"""


class BaseDataSource:
    def __init__(self, name):
        self.name = name
        self.results = {}

    def query(self, key, update: bool = False):
        key = self.sanitize(key)
        key_parts = key.split("|")
        root_key = key_parts[0]

        if root_key not in self.results or update:
            self.results[root_key] = self.find(root_key)

        return self.by_key(key)

    def find(self, key, exclude=None):
        raise NotImplementedError

    def by_key(self, key):
        key = self.sanitize(key)
        key_parts = key.split("|")
        root_key = key_parts[0]
        result = self.results.get(root_key)

        if not result:
            return

        if len(key_parts) == 1:
            return result

        if key not in result:
            return

        if len(key_parts) > 1:
            if not result.get(key):
                result = dict(
                    list(filter(lambda r: r[0].startswith(key), result.items()))
                )
                result.pop(key)
            else:
                result = result.get(key)

        return result

    def sanitize(self, key):
        raise NotImplementedError
