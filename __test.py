#   coding: utf-8
#   test

import json
import sys
import io

# from products.maxcompute.libs.dic2tree import data1
from tools import load_input_data
from tools import TreeTool

reload(sys)
sys.setdefaultencoding('utf8')


if __name__ == '__main__':
    file_name = "data.txt"
    file_object = io.open(file_name, "r", encoding='utf-8')
    content = ''
    try:
        for line in file_object.readlines():
            content += line
    finally:
        file_object.close()
    in_data = json.loads(content)

    group_by = ["region", "public_region_name", "datacenter", "cluster"]

    # in_data = load_input_data()
    # labels = ["net_region", "region_name", "area", "cluster"]
    # tt = TreeTool(group_by, "odps", in_data, strategy_name="odps")
    # extra_data = data1.extra_data
    tt = TreeTool(group_by, "odps", in_data, strategy_name="odps")
    print("new: " + json.dumps(tt.get_tree("odps")))

    path = {
        "path": ["odps", "cn"],
        }
    tree = tt.get_sub_tree_by_path(path, transformer="odps")
    print("new1: " + json.dumps(tree))

    # path = {
    #     "path":["blink", "PRODUCT", "集团"],
    # }
    # sub_tree = tt.get_sub_tree_by_path(path)
    # print("sub: " + json.dumps(sub_tree))
    #
    # var ={
    #      "conditions": {"label": "PRODUCT", "level": 1},
    #      "field": "ext_data",
    #      "data": 'tjlcast'
    #      }
    #
    # var2 ={
    #      "conditions": {"label": "PRODUCT", "level": 1},
    #      "field": "ext_data",
    #      }
    # tt.set_data(var)
    # print(json.dumps(tt.get_tree()))
    # print(tt.get_data(var2))
    #
    # var3 = {
    #     "level":2,
    #     "key":"region_name",
    #     "value":"公共云",
    #     "is_leaf":True
    # }
    # print(json.dumps(tt.get_sub_tree(var3)))






