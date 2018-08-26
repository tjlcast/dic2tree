#   coding: utf-8
import json

from test import data2
from test import data3
from tools import StructuredDataTool

if __name__ == "__main__":
    data = data2.data2
    tt = StructuredDataTool().loadData(data).build()
    # print json.dumps(tt.get_tree())

    tt = StructuredDataTool().loadData(data).rich_infos(data3.data3).build()
    print json.dumps(tt.get_tree())