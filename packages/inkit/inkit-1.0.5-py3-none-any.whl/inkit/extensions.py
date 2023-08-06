import base64


class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def flat(data):
    if isinstance(data, list):
        return [flat(item) for item in data]

    if isinstance(data, dict):
        return AttrDict({key: flat(val) for key, val in data.items()})

    return data


def base64encode(value):
    if isinstance(value, str):
        value = value.encode('utf-8')
    return base64.b64encode(value).decode('utf-8')
