#   coding: utf-8
#   blink的转换器

from load_transfomer import transform


"""
        dfs 后序
        输入的node_map格式为：
        id          [int]   当前节点的唯一id
        key         [str]   分组的字段名
        field       [str]   分组的val
        label       [str]   用于给前端展示的值，采用field的值
        value       [str]   用于前端与后端的交互数据，采用field的值
        parent_id   [int]   当前节点的父节点
        level       [int]   当前节点的深度
        children    [dict]  子节点 {分组的val -> 节点}
        is_leaf     [boolean]   是否是叶子节点
        ext_data   [null or list or obj]    在叶子节点存放了，输入数据 {list} 的一个元素
        """


@transform("blink")
def blink_func(node_map):
    new_node = {"id": node_map["id"],
                "label": node_map["label"],
                "value": node_map["value"],
                "key": node_map["key"],
                "children": [],
                "parent_id": node_map["parent_id"],
                "is_leaf": node_map["is_leaf"],
                "level": node_map["level"],
                "isCollapsed": False,
                "ext_data": node_map["ext_data"]}

    # 处理children,把原始的dict转化为list
    if node_map['children'] and type(node_map['children']).__name__ == 'dict':
        new_node['children'] = node_map['children'].values()

    # 处理ext_data, 把原始的list转化为dict
    if type(node_map["ext_data"]).__name__ == "list":
        new_node["ext_data"] = {}
        for ext_data_item in node_map["ext_data"]:
            tmp_dict = ext_data_item
            if type(ext_data_item).__name__ == dict:
                tmp_dict = {k: v for k,v in ext_data_item.items}
            new_node["ext_data"] = tmp_dict
    return new_node


odps_global_region_name_mapper = {}


@transform("odps")
def odps_func(node_map):
    new_node = {"id": node_map["id"],
                "label": node_map["label"],
                "value": node_map["value"],
                "key": node_map["key"],
                "children": [],
                "parent_id": node_map["parent_id"],
                "is_leaf": node_map["is_leaf"],
                "level": node_map["level"],
                "isCollapsed": False,
                "ext_data": node_map["ext_data"]}

    # 把深度 >= 3 的节点 isCollapsed 设为true
    if int(new_node["level"]) > 2:
        new_node["isCollapsed"] = True

    # 处理children,把原始的dict转化为list
    if node_map['children'] and type(node_map['children']).__name__ == 'dict':
        new_node['children'] = node_map['children'].values()

    # 处理ext_data, 把原始的list转化为dict
    if type(node_map["ext_data"]).__name__ == "list":
        new_node["ext_data"] = {}
        for ext_data_item in node_map["ext_data"]:
            tmp_dict = ext_data_item
            if type(ext_data_item).__name__ == dict:
                tmp_dict = {k: v for k,v in ext_data_item.items}
            new_node["ext_data"] = tmp_dict

    # 对root 节点的 children 进行排序，集团弹内-中国公共云-新加坡弹内 cn-internal - cn - sg-internal
    def region_sort(elem):
        if elem.get("value") == "cn-internal":
            return 10
        elif elem.get("value") == "cn":
            return 9
        elif elem.get("value") == "sg-internal":
            return 8
        else:
            return 0
    if new_node.get("key") == "product":
        new_node.get("children").sort(key=region_sort, reverse=True)

    return new_node


if __name__ == "__main__":
    g = blink_func.__group__
    print(g)
