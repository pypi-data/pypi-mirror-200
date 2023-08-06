import json
import requests


# 根据产品名称查询产品下的设备数,返回设备列表与设备信息列表
def queryDeviceIdUnderProduct(ip, port, productName):
    url = "http://" + ip + ":" + port + "/mach/device/instance/_query"
    payload = json.dumps({
        "terms": [
            {
                "termType": "eq",
                "column": "product_id",
                "value": productName
            }
        ],
        "includes": [
            "id"
        ]
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': ip + ":" + port,
        'Connection': 'keep-alive'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    device_List = []
    device_Property = {}
    if response:
        json_dic = response.json()
        result = json_dic["result"]
        number = result["total"]

        for i in range(number):
            device_List.append(result["data"][i]["id"])
            property_dic = {}
            for pro in result["data"][i]["tags"]:
                property_dic.update({pro["key"]: pro["value"]})
            device_Property.update({result["data"][i]["id"]: property_dic})
    return device_List, device_Property
