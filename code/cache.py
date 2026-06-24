
class Cache:
    def __init__(self, dict_: dict):
        self.cache = set(dict_.items())

    def make_cache(self, new_dict):
        self.cache = set(new_dict.items())

    def clear_cache(self):
        self.cache.clear()


def cache(func):
    pass

