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


def build_tree(fields, input_datas, root, extra_data=None, strategy_name="default"):
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
            strategy(node, new_node, item, extra_data)
            node = new_node
        node.is_leaf = True
        if not node.ext_data:
            node.ext_data = []
        if type(node.ext_data).__name__ == "list":
            node.ext_data.append(item)
    return root


def parse_tree(tree, transform="default"):
    """
    把字典树转化为通用结构体
    :param tree:            字典树的root
    :param transform:       配置的解析器,注意要小写
    :return:
    """
    return tree.to_struct(transform)


def __dfs(data, root, __action):
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
    :param data: 是从根节点开始的
    :param root:
    :param __action:
    :return:
    """
    path = data["conditions"]["path"]
    node = root
    for pre_node_str in path[1:]:
        # pre_node_str = urllib.unquote(str(pre_node_str)).decode('utf8')
        print("path==============" +pre_node_str)
        print("children==============" + str(node.children.keys()))
        for key in node.children.keys():
            if key == pre_node_str:
                node = node.children[key]
        #node = node.children[pre_node_str]
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
    __dfs(info, tree, action)
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
    def __init__(self, field, product_str, input_datas, extra_data=None, strategy_name="default"):
        """
        构造器
        :param field:           分组时使用字段
        :param product_str:     root node的信息，一般为产品线
        :param input_datas:     使用的数据<[{}]>
        """
        tree = build_tree(field, input_datas, TriTree("", "", None, 0), extra_data, strategy_name)
        tree.key = "product"
        tree.value = product_str
        tree.label = product_str
        self.tree = tree

    def get_tree(self, transformer="blink"):
        tree = self.tree
        parsed_tree = parse_tree(tree, transformer)
        return parsed_tree

    def get_sub_tree(self, params, transformer="blink"):
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
           把字典树中，根据层数和label来修改字典树节点的指定值
           :param input_data:
           {
           "conditions": {"key"<str>, "value"<str>,"level"<int>} 对比字段,逻辑链接为"与", result:yes | no
           "field"<str>
           "data"<obj>
           }
           :param tree:    字典树的root
           :return:
           """
        tree = self.tree
        self.tree = set_data_to_tree(input_data, tree)

    def get_data(self, input_data):
        """
            把字典树中，根据层数和字段得到字典树节点的指定值
                :param input_data:
                {
                "conditions": {"key"<str>, "value"<str>,"level"<int>} 对比字段,逻辑链接为"与", result:yes | no
                "field"<str>
                }
            :param tree:    字典树的跟
            :return:
            """
        tree = self.tree
        val = get_data_from_tree(input_data, tree)
        return val

    def get_sub_tree_by_path(self, params, transformer="blink"):
        """
        得到子树
        :param params:<dict>
            path:<list>
        :param transformer:
        :return:
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
                   把字典树中，根据层数和label来修改字典树节点的指定值
                   :param input_data:
                   {
                   "conditions": {"path"<list>, } 树节点的前缀, result:yes | no
                   "field"<str>
                   "data"<obj>
                   }
                   :param tree:    字典树的root
                   :return:
                   """
        tree = self.tree
        self.tree = set_data_to_tree_py_path(input_data, tree)

    def get_data_by_path(self, input_data):
        """
            把字典树中，根据层数和字段得到字典树节点的指定值
                :param input_data:
                {
                "conditions": {"key"<str>, "value"<str>,"level"<int>} 对比字段,逻辑链接为"与", result:yes | no
                "field"<str>
                }
            :param tree:    字典树的跟
            :return:
            """
        tree = self.tree
        val = get_data_from_tree_by_path(input_data, tree)
        return val
