#   coding: utf-8
#   通用工具


class ObjUtils:
    def __init__(self):
        pass

    @classmethod
    def get_class_name(cls, obj):
        return type(obj).__name__

    @classmethod
    def obj_belong2class(cls, obj, clz):
        return isinstance(obj, clz)
