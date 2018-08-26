#   coding: utf-8
#   test

import json
import sys
import io

from data1 import extra_data
from tools import GroupByTool

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

    tt = GroupByTool().loadData(group_by, "odps", in_data, extra_data=extra_data, strategy_name="odps").build()
    print("new: " + json.dumps(tt.get_tree("odps")))

    path = {
        "path": ["odps", "cn"],
        }
    tree = tt.get_sub_tree_by_path(path, transformer="odps")
    print("new1: " + json.dumps(tree))







