import json
from flask import Flask, request, jsonify
from elasticsearch8 import Elasticsearch
from pathlib import Path

def construct_query(params):
    query = {"bool": {"must": []}}

    # 添加查询条件（仅当相关参数不为空时）
    if "healthAdvice" in params and params["healthAdvice"]:
        query["bool"]["must"].append({"match": {"healthAdvice": params["healthAdvice"]}})

    if "averageValue" in params and params["averageValue"]:
        query["bool"]["must"].append({"match": {"averageValue": params["averageValue"]}})

    if "healthParameter" in params and params["healthParameter"]:
        query["bool"]["must"].append({"match": {"healthParameter": params["healthParameter"]}})

    if "siteName" in params and params["siteName"]:
        query["bool"]["must"].append({"match": {"siteName": params["siteName"]}})

    if "startHour" in params and "endHour" in params:
        start_hour = params["startHour"]
        end_hour = params["endHour"]

        # 设定小时范围的时间段
        query["bool"]["must"].append({
            "range": {
                "timestamp": {
                    "gte": f"{start_hour}:00:00",
                    "lte": f"{end_hour}:00:00"
                }
            }
        })

    return query

def main():
    # 从查询字符串中获取参数
    date_str = request.args.get('date', None)  # 提取日期参数
    start_hour = request.args.get('startHour', None)  # 开始小时
    end_hour = request.args.get('endHour', None)  # 结束小时

    # 创建Elasticsearch客户端
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    # 构建索引名称
    if date_str:
        index_name = f"epa-air-quality-{date_str}"
        output_file_path = Path(f"./epa-air-quality-results-{date_str}.json")
    else:
        index_name = "epa-air-quality-*"
        output_file_path = Path(f"./epa-air-quality-results-all.json")

    # 构建查询
    params = {
        "startHour": start_hour,
        "endHour": end_hour,
        "healthAdvice": request.args.get("healthAdvice", None),
        "averageValue": request.args.get("averageValue", None),
        "healthParameter": request.args.get("healthParameter", None),
        "siteName": request.args.get("siteName", None),
    }

    query = construct_query(params)

    # 执行Elasticsearch查询
    res = client.search(index=index_name, query=query)

    # 将结果存储到JSON文件
    with output_file_path.open("w") as f:
        json.dump(res, f, indent=2)

    return jsonify({"message": f"Results saved to {output_file_path}"})
