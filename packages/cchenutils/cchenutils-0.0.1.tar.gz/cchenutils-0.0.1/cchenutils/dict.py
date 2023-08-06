import json


class dict(dict):
    def nget(self, key, default=None):
        # nested get
        if '/' in key:
            k1, k2 = key.split('/', 1)
            return dict(self[k1]).nget(k2) if self[k1] else None
        else:
            return json.dumps(self[key]) if isinstance(self.get(key), (dict, list)) else self.get(key)

    def gets(self, keys, default=None):
        # nested gets
        return [self.nget(k, default.get(k)) for k in keys] if default else [self.nget(k) for k in keys]

    @property
    def __class__(self):
        return dict
