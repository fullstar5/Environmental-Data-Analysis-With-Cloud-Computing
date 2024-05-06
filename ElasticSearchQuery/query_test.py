import json
from flask import Flask, request, jsonify
from elasticsearch8 import Elasticsearch
from pathlib import Path

def construct_query(params):
    query = {"bool": {"must": []}}

    if "startDate" in params and "endDate" in params:
        start_date = params["startDate"]
        end_date = params["endDate"]

        query["bool"]["must"].append({
            "range": {
                "timestamp": {
                    "gte": f"{start_date}T00:00:00",
                    "lte": f"{end_date}T23:59:59"
                }
            }
        })

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
    start_date = request.args.get("startDate", None)
    end_date = request.args.get("endDate", start_date)  # 默认使用 start_date 作为 end_date
    start_hour = request.args.get('startHour', None)
    end_hour = request.args.get('endHour', None)

    # connect to ES
    try:
        client = Elasticsearch(
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs=False,
            basic_auth=('elastic', 'elastic'),
            timeout=60,
            ssl_show_warn=False
        )
    except Exception as e:
        print("error when connect with ES: ", e)
        return 500

    # if exact date given
    if end_date:
        index_name = f"epa-air-quality-{start_date}-{end_date}"
        output_file_path = Path(f"./epa-air-quality-results-{start_date}-{end_date}.json")
    # else:
    #     index_name = "epa-air-quality-*"
    #     output_file_path = Path(f"./epa-air-quality-results-all.json")

    # construct params
    params = {
        "startHour": start_hour,
        "endHour": end_hour,
        "healthAdvice": request.args.get("healthAdvice", None),
        "averageValue": request.args.get("averageValue", None),
        "healthParameter": request.args.get("healthParameter", None),
        "siteName": request.args.get("siteName", None),
    }

    # query and dump into json file
    query = construct_query(params)
    size = 10000  # query size
    res = client.search(index=index_name, query=query, size=size)

    with output_file_path.open("w") as f:
        json.dump(res, f, indent=2)

    return jsonify({"message": f"Results saved to {output_file_path}"})
