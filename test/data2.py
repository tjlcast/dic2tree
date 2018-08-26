#   coding:utf-8

import json


data2 = """[
{
"name": "错误",
"parent": 0,
"author": "NULL",
"created": null,
"modified": null,
"id": 2
},
{
"name": "问题",
"parent": 0,
"author": "NULL",
"created": null,
"modified": null,
"id": 3
},
{
"name": "可感知错误",
"parent": 2,
"author": "NULL",
"created": null,
"modified": "2016-03-21 19:25:30",
"id": 4
},
{
"name": "不可感知错误",
"parent": 2,
"author": "NULL",
"created": null,
"modified": null,
"id": 5
},
{
"name": "instance错误",
"parent": 5,
"author": "NULL",
"created": null,
"modified": "2016-02-24 10:50:03",
"id": 6
},
{
"name": "已知风险",
"parent": 3,
"author": "NULL",
"created": null,
"modified": null,
"id": 7
},
{
"name": "core dump",
"parent": 7,
"author": "NULL",
"created": null,
"modified": null,
"id": 8
},
{
"name": "odps错误",
"parent": 4,
"author": "NULL",
"created": "2016-01-25 20:26:18",
"modified": "2016-02-24 10:49:55",
"id": 9
},
{
"name": "基线1956",
"parent": 1,
"author": "NULL",
"created": "2016-02-19 16:57:38",
"modified": "2016-02-19 16:57:38",
"id": 10
},
{
"name": "tunnel",
"parent": 1,
"author": "NULL",
"created": "2016-02-19 17:22:20",
"modified": "2016-02-19 17:22:20",
"id": 11
},
{
"name": "HBO",
"parent": 1,
"author": "NULL",
"created": "2016-02-23 17:16:12",
"modified": "2016-02-23 17:16:12",
"id": 12
},
{
"name": "MR",
"parent": 1,
"author": "NULL",
"created": "2016-02-23 17:26:02",
"modified": "2016-02-23 17:26:02",
"id": 13
},
{
"name": "问题机器",
"parent": 7,
"author": "NULL",
"created": "2016-02-23 17:30:28",
"modified": "2016-02-23 17:30:28",
"id": 14
},
{
"name": "潜在风险",
"parent": 3,
"author": "NULL",
"created": "2016-02-23 17:42:41",
"modified": "2016-02-23 17:42:41",
"id": 15
},
{
"name": "fuxi指标",
"parent": 15,
"author": "NULL",
"created": "2016-02-23 17:43:20",
"modified": "2016-02-23 17:43:20",
"id": 16
},
{
"name": "pangu指标",
"parent": 15,
"author": "NULL",
"created": "2016-02-23 17:43:32",
"modified": "2016-02-23 17:43:32",
"id": 17
},
{
"name": "odps指标",
"parent": 15,
"author": "NULL",
"created": "2016-02-23 17:43:56",
"modified": "2016-02-23 17:43:56",
"id": 18
},
{
"name": "job错误",
"parent": 5,
"author": "NULL",
"created": "2016-02-24 10:50:16",
"modified": "2016-02-24 10:50:16",
"id": 19
},
{
"name": "核心基线",
"parent": 1,
"author": "NULL",
"created": "2016-02-24 15:50:30",
"modified": "2016-02-24 15:50:30",
"id": 20
},
{
"name": "跨集群复制",
"parent": 1,
"author": "NULL",
"created": "2016-02-24 18:05:04",
"modified": "2016-02-24 18:05:04",
"id": 21
},
{
"name": "实时监控",
"parent": 0,
"author": "NULL",
"created": "2016-03-08 19:12:49",
"modified": "2016-03-08 19:12:49",
"id": 22
},
{
"name": "蚂蚁基线",
"parent": 1,
"author": "NULL",
"created": "2016-05-09 18:21:43",
"modified": "2016-05-09 18:21:43",
"id": 23
},
{
"name": "sql_flighting",
"parent": 1,
"author": "NULL",
"created": "2016-11-03 21:54:35",
"modified": "2016-11-10 19:11:00",
"id": 24
},
{
"name": "s27_sql_flighting",
"parent": 1,
"author": "NULL",
"created": "2016-11-10 19:12:17",
"modified": "2017-04-24 12:22:33",
"id": 25
},
{
"name": "summary",
"parent": 1,
"author": "NULL",
"created": "2016-11-11 17:49:37",
"modified": "2016-11-26 13:32:42",
"id": 26
},
{
"name": "线上Release",
"parent": 1,
"author": "NULL",
"created": "2016-11-25 18:49:24",
"modified": "2016-11-25 18:49:24",
"id": 27
},
{
"name": "ServiceMode任务",
"parent": 1,
"author": "NULL",
"created": "2016-11-30 16:24:51",
"modified": "2016-12-06 15:28:26",
"id": 28
},
{
"name": "非ServiceMode任务",
"parent": 1,
"author": "NULL",
"created": "2016-11-30 16:25:28",
"modified": "2016-12-06 15:28:18",
"id": 29
},
{
"name": "控制集群耗时",
"parent": 1,
"author": "NULL",
"created": "2017-03-29 17:30:17",
"modified": "2017-03-29 17:30:17",
"id": 30
},
{
"name": "Opp",
"parent": 1,
"author": "NULL",
"created": "2017-03-29 17:30:17",
"modified": "2017-03-29 17:30:17",
"id": 31
},
{
"name": "混部SLA",
"parent": 1,
"author": "NULL",
"created": "2017-12-29 17:39:08",
"modified": "2017-12-29 17:39:08",
"id": 32
},
{
"name": "集群Backup成功率",
"parent": 1,
"author": "NULL",
"created": "2018-01-03 19:21:36",
"modified": "2018-01-03 19:21:36",
"id": 33
}
]
"""
data2 = json.loads(data2)
