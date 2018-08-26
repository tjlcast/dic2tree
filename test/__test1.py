#   coding: utf-8
import json

from builder import StructuredDataTool
from test import data2
from test import data3

if __name__ == "__main__":
    data = data2.data2
    tt = StructuredDataTool().loadData(data).build()
    # print json.dumps(tt.get_tree())

    tt = StructuredDataTool().loadData(data).rich_infos(data3.data3).build()
    print json.dumps(tt.get_tree())

    param = {
        "path": [0, 3, 15, 18]
    }
    rs = tt.get_sub_tree_by_path(param)
    print json.dumps(rs)
