from collections import defaultdict
from decimal import Decimal
import json


class Scripts:

    def __init__(self, num_list: list[float] | None=None):
       
        self.num_list = num_list if num_list is not None else [1,2]

    @property
    def sum_list(self)->Decimal:
        return sum(self.num_list)

    def word_count(self, text:str) -> int:
        return len(text.split())
    
    def group_by_key(self, dict_list:list[dict])-> dict:
        grouped_dict = defaultdict(list)
        for item in dict_list:
            # grouped_dict[f"customer_id_{item["customer_id"]}"].update({key: value for key,value in item.items() if key!= f"customer_id"})
            grouped_dict[f"customer_id_{item["customer_id"]}"].append({key: value for key,value in item.items() if key!= f"customer_id"})
        return dict(grouped_dict)

    def validate_data(self, datalist:list[dict]) ->list[dict]:
        filtered_data = []
        # for item in datalist:
        #     if "money" in item and item["money"] >= 0 and "kwh" in item and item["kwh"] >=0:
        #         filtered_data.append(item)
        filtered_data = [
            item for item in datalist
            if ("kwh" in item
            and item["kwh"] >= 0 or "kwh" not in item)
            and ("money" in item
            and item["money"] >= 0 or "money" not in item)
        ]
        return filtered_data

    def read_json_file(self, path:str) -> dict:
        with open(path, "r") as f:
            json_data = json.load(f)
            return json_data["customers"][0]

if __name__ == "__main__":
    scripts_obj = Scripts([1,2,3,4,5,7.5])
    print(scripts_obj.sum_list)
    print(scripts_obj.word_count("hello world from python"))
    print(scripts_obj.group_by_key([
        {
            "customer_id":1,
            "name": "user 1",
            "money": 12
        },
        {
            "customer_id":3,
            "name": "user 3",
            "money": 5
        },
        {
            "customer_id":1,
            "job": "job 1",
            "description": "this is fucking discription"
        },

    ]))
    print(scripts_obj.validate_data([
        {"customer_id": 1, "kwh": 100, "money": 50},
        {"customer_id": 2, "kwh": -10, "money": 20},   # invalid — negative kwh
        {"customer_id": 3, "kwh": 50, "money": -5},    # invalid — negative money
        {"customer_id": 4, "name": "no usage fields"}, # valid — no kwh/money keys
        {"customer_id": 5, "kwh": 0, "money": 0},     # valid — zero is OK
        {"customer_id": 2, "kwh": -10}
    ]))
    print(scripts_obj.read_json_file("prep/data.json"))

