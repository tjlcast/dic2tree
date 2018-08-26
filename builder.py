#   coding:utf-8
#   builder 构建器

from TriTree import TriTree
from strategies_load import strategies
from tools import TreeTool

"""
    数据工具的构建器:
        AbstractBuilder，为抽象对象，提供 build
        通过基继承AbstractBuilder，并提供对root、nodes_mapper、tree的实例化
    usage: 
        StructuredDataTool().loadData(data).build()
"""


class AbstractBuilder(object):
    def __init__(self):
        self.root = TriTree("", "", None, 0)
        self.nodes_mapper = dict()
        self.nodes_mapper.setdefault(self.root.id, self.root)
        self.tree = None

    def build(self):
        """
        由用户自己在该对象中生成: root、node_mapper、tree

        :return:
        """
        root = self.root
        nodes_mapper = self.nodes_mapper
        tree = self.tree
        return TreeTool(root, nodes_mapper, tree)


class GroupByTool(AbstractBuilder):
    def __init__(self):
        AbstractBuilder.__init__(self)

    def __build_tree(self, fields, input_datas, root, extra_data=None, strategy_name="default"):
        """
        创建字典树
        :param fields:          分组操作依据的字段 [list]
        :param input_datas:     分组操作处理的数据 [list + dict]
        :param root:
        :return:                生成的字典树
        """
        strategy = strategies[strategy_name]
        items = input_datas

        for item in items:
            node = root
            for field in fields:
                label = item[field]
                new_node = node.get_or_create(label, field)
                self.nodes_mapper.setdefault(new_node.id, new_node)
                strategy(node, new_node, item, extra_data)
                node = new_node
            node.is_leaf = True
            if not node.ext_data:
                node.ext_data = []
            if type(node.ext_data).__name__ == "list":
                node.ext_data.append(item)
        return root

    def loadData(self, field, product_str, input_datas, extra_data=None, strategy_name="default"):
        """
        :param field:           分组时使用字段
        :param product_str:     root node的信息，一般为产品线
        :param input_datas:     使用的数据<[{}]>
        :param extra_data:      传到 strategy 的参数
        :param strategy_name:   选用的 strategy 名字
        :return:
        """
        tree = self.__build_tree(field, input_datas, self.root, extra_data, strategy_name)
        tree.key = "product"
        tree.value = product_str
        tree.label = product_str
        self.tree = tree
        return self


class StructuredDataTool(AbstractBuilder):
    def __init__(self):
        AbstractBuilder.__init__(self)

    def __build_tree(self):
        pass

    def __build_node(self, id, tmp_nodes_dict, strategy_name="default", extra_data=None):
        if self.nodes_mapper.__contains__(id):
            return self.nodes_mapper.get(id)

        node_info = tmp_nodes_dict.get(id)
        if not node_info:
            return None

        parent = node_info.get("parent")
        parent_node = self.__build_node(parent, tmp_nodes_dict)
        if not parent_node:
            return None

        node = TriTree("None", "None", parent, -1)
        node.id = id
        self.nodes_mapper[id] = node
        node.value = node_info
        node.level = parent_node.level + 1
        node.is_leaf = True
        node.ext_data = []
        parent_node.children[id] = node
        parent_node.is_leaf = False

        strategy = strategies[strategy_name]
        strategy(parent_node, node, node_info, extra_data)
        return node

    def loadData(self, other_nodes, strategy_name="default", extra_data=None):
        """
        通过传入的数据生成: root, nodes_mapper, tree
        :return:
        """
        self.nodes_mapper.pop(self.root.id)
        self.root.id = 1
        self.root.parent_id = -1
        self.root.ext_data = []
        self.nodes_mapper.setdefault(self.root.id, self.root)

        tmp_nodes_dict = dict()
        for node in other_nodes:
            id = node.get("id")
            tmp_nodes_dict.setdefault(id, node)

        for k, v in tmp_nodes_dict.items():
            self.__build_node(k, tmp_nodes_dict, strategy_name, extra_data)

        tree = self.root
        tree.key = "product"
        tree.value = "none"
        tree.label = "none"
        self.tree = tree
        return self

    def rich_infos(self, infos):
        for info in infos:
            node_id = info.get("parent")
            while self.nodes_mapper.__contains__(node_id):
                node = self.nodes_mapper.get(node_id)
                node.ext_data.append(info)
                node_id = node.parent_id
        return self

