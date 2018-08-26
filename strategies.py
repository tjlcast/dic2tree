#   coding: utf-8
#   blink的转换器

import json
from strategies_load import strategy

""" 
        pnode 为父节点
        cnode 为当前节点
        line_entity 为当期处理的那一行数据
        
        输入的node格式为：
        
        输入的node_map格式为：
        id          [int] 当前节点的唯一id
        key         [str] 分组的字段名
        
        field       [str] 分组的字段名
        label       [str] 分组的val
        
        value       [str] 分组的val
        parent_id   [int] 当前节点的父节点
        level       [int] 当前节点的深度
        children    [dict] 子节点 {分组的val -> 节点}
        is_leaf     False 无效的
        ext_data   [none or list or obj] 在叶子节点存放了，输入数据 {list} 的一个元素
        
        重要 - 重要 - 重要：
        不要修改结构字段：field: id, key, parent_id, level, children, is_leaf
"""


@strategy("odps")
def odps_func(pnode, cnode, line_entity, extra_data):
    if 'region' == cnode.key:
        cnode.value = line_entity["region"]
        cnode.label = line_entity["region_name"]
    pPath = pnode.path if hasattr(pnode, "path") else ""
    pPath = (pPath + "/" + cnode.value)
    cnode.path = pPath.strip('/')

    extra_data_item = extra_data.get(cnode.path, {"inf": ""})["inf"]
    if extra_data_item:
        cnode.ext_data = {
            "summary": json.loads(extra_data_item),
            "detail": {}
        }


if __name__ == "__main__":
    pass
