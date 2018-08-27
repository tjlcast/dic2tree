#   coding: utf-8


class NotSupportParamException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, args, kwargs)


if __name__ == "__main__":
    pass
