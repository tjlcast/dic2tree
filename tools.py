#   coding: utf-8
#   tools

from strategies_load import strategies
from TriTree import TriTree
import io
import sys
import json

reload(sys)
sys.setdefaultencoding('utf8')


def load_input_data(file_name='data.txt'):
    """
    加载数据，并把数据封装成[{}]的形式
    :param file_name:   加载的数据文件名，导入一张二维的表
    :return:            封装的数据
    """
    file_object = io.open(file_name, "r", encoding='utf-8')
    try:
        items = []
        line = file_object.readline()
        fields = line.split("\t")

        for line in file_object.readlines():
            vals = line.split("\t")
            a = zip(fields, line)
            item = dict(zip(fields, vals))
            items.append(item)
            pass
        return items
    finally:
        file_object.close()


def load_input_data1(file_name="data1.txt"):
    file_object = io.open(file_name, "r", encoding='utf-8')
    try:
        content = file_object.read()
        items = json.loads(content)
        return items
    finally:
        file_object.close()


def parse_tree(tree, transform="default"):
    """
    把字典树转化为通用结构体
    :param tree:            字典树的root
    :param transform:       配置的解析器,注意要小写
    :return:
    """
    return tree.to_struct(transform)


def __dfs(data, root, __action):
    """
    dfs遍历，根据节点中的字段进行
    :param data:
    :param root:
    :param __action:
    :return:
    """
    level = data["conditions"]["level"]
    if root.level > level:
        return
    if root.level < level:
        for child in root.children.values():
            __dfs(data, child, __action)
        return
    for k, v in data['conditions'].items():
        if not root.__dict__.__contains__(k) or root.__dict__[k] != v:
            return
    # 处理执行动作
    __action.do(data, root)
    return


def __dfs_prefix(data, root, __action):
    """
    是从根节点开始的,节点的遍历通过children的key进行
    :param data:
    :param root:
    :param __action:
    :return:
    """
    path = data["conditions"]["path"]
    node = root
    for pre_node_str in path[1:]:
        for key in node.children.keys():
            if key == pre_node_str:
                node = node.children[key]
    __action.do(data, node)
    return


def set_data_to_tree(input_data, tree):
    class __Action:
        def __init__(self):
            self.result = None

        def do(self, data, root):
            root.__dict__[data["field"]] = data["data"]
    action = __Action()
    info = input_data
    __dfs(info, tree, action)
    return tree


def get_data_from_tree(input_data, tree):
    class __Action:
        def __init__(self):
            self.result = None

        def do(self, data, root):
            self.result = root.__dict__[data["field"]]
    action = __Action()

    info = input_data
    __dfs(info, tree, action)
    return action.result


def get_sub_tree(input_data, tree):
    """
    得到树的某个子树
    :param input_data:
    {
        "conditions": {"key"<str>, "value"<str>, "level"<int>} 对比字段,逻辑链接为"与", result:yes | no
    }
    :param tree:
    :return:
    """
    class __Action:
        def __init__(self):
            self.result = None

        def do(self, data, root):
            self.result = root
    action = __Action()
    info = input_data
    __dfs(info, tree, action)
    return action.result


def get_data_from_tree_by_path(input_data, tree):
    class __Action:
        def __init__(self):
            self.result = None

        def do(self, data, root):
            self.result = root.__dict__[data["field"]]
    action = __Action()

    info = input_data
    __dfs_prefix(info, tree, action)
    return action.result


def set_data_to_tree_py_path(input_data, tree):
    class __Action:
        def __init__(self):
            self.result = None

        def do(self, data, root):
            root.__dict__[data["field"]] = data["data"]
    action = __Action()
    info = input_data
    __dfs_prefix(info, tree, action)
    return tree


def get_sub_tree_by_path(input_data, tree):
    """
    根据树节点的前缀得到子树
    :param input_data:
    :param tree:
    :return:
    """
    class __Action:
        def __init__(self):
            self.result = None

        def do(self, data, root):
            self.result = root

    action = __Action()
    info = input_data
    __dfs_prefix(info, tree, action)
    return action.result


class TreeTool:
    def __init__(self, root, node_mapper, tree):
        self.root = root
        self.node_mapper = node_mapper
        self.tree = tree

    def get_tree(self, transformer="defult"):
        tree = self.tree
        parsed_tree = parse_tree(tree, transformer)
        return parsed_tree

    def get_sub_tree(self, params, transformer="defult"):
        """
        得到子树
        :param params:          <dict> 包含level、key、value 三个字段
        :param transformer:     <str>  转换tree使用的转换器
        :return:
        """
        level_int = int(params["level"])
        key_str = params["key"]
        value_str = params["value"]

        conds = {
            "conditions": {
                "level": level_int,
                "key": key_str,
                "value": value_str,
            }
        }
        tree = self.tree
        tree = get_sub_tree(conds, tree)
        parsed_tree = parse_tree(tree, transformer)
        return parsed_tree

    def set_data(self, input_data):
        """
        给节点设置值，根据层数和label来修改|设置字典树节点的指定值
        :param input_data:
            {"key"<str>, "value"<str>,"level"<int>} 对比字段,逻辑链接为"与"
        :return:
        """
        tree = self.tree
        self.tree = set_data_to_tree(input_data, tree)

    def get_data(self, input_data):
        """
        得到节点中的值，根据层数和字段得到字典树节点的指定值
        :param input_data:{
                "conditions": {"key"<str>, "value"<str>,"level"<int>} 对比字段,逻辑链接为"与", result:yes | no
                "field"<str>
                }
        :return:
        """
        tree = self.tree
        val = get_data_from_tree(input_data, tree)
        return val

    def get_sub_tree_by_path(self, params, transformer="default"):
        """
        得到子树, 根据节点的路径
        :param params: {
            "path": <列表>, 节点的children 的 key
        }
        :param transformer:
        :return: 得到的子树
        """
        path = params["path"]

        conds = {
            "conditions": {
                "path": path
            }
        }
        tree = self.tree
        tree = get_sub_tree_by_path(conds, tree)
        parsed_tree = parse_tree(tree, transformer)
        return parsed_tree

    def set_data_by_path(self, input_data):
        """
        给节点设置value，根据节点的前缀路径
        :param input_data: {
                   "conditions": {"path"<list>, } 树节点的前缀
                   "field"<str>
                   "data"<obj>
                   }
        :return: None
        """
        tree = self.tree
        self.tree = set_data_to_tree_py_path(input_data, tree)

    def get_data_by_path(self, input_data):
        """
        得到节点的属性值, 根据节点的前缀路径
        :param input_data:{
                   "conditions": {"path"<list>, } 树节点的前缀,
                   "field"<str>
                   }
        :return: 对应的值
        """
        tree = self.tree
        val = get_data_from_tree_by_path(input_data, tree)
        return val

    def add_nodes(self):
        # todo
        pass
