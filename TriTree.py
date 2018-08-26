#   coding: utf-8
#   字典树

import uuid
from load_transfomer import handlers
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class TriTree:
    def __init__(self, label, field, parent_id, level, is_leaf=False):
        self.id = uuid.uuid4().__str__()
        self.label = label
        self.value = label
        self.key = field
        self.parent_id = parent_id
        self.level = level
        self.children = dict()
        self.field = field

        self.is_leaf = is_leaf
        self.ext_data = None     # 该字段在叶子节点装载了分组中的每条数据

    def node_transform(self, node_map, transform):
        if handlers is not None and handlers.__contains__(transform):
            node_map = handlers[transform](node_map)
        return node_map

    def get_or_create(self, input_label, input_field):
        node = TriTree(input_label, input_field, self.id, self.level+1)
        node = self.children.setdefault(input_label, node)
        return node

    def to_struct(self, transform="default"):
        node_map = dict(self.__dict__)
        node_map["children"] = dict()
        if not self.is_leaf:
            for key in self.children.keys():
                node_map["children"][key] = self.children[key].to_struct(transform)

        node_map = self.node_transform(node_map, transform)
        return node_map
