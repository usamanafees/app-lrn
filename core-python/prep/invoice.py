# from collections import defaultdict
from typing import List
from billing import LineItem

class Invoice:
    def __init__(self):
        self.item_list: List[LineItem] = []

    def add_items(self, items_list: List[LineItem]):
        self.item_list = items_list

    @property
    def totalBill(self) -> float:
        return sum(x.total for x in self.item_list)
    
    def total_by_customer(self) -> dict:
        total_by_customer:dict = {}
        # for i in range(len(self.item_list)):
        #     if f"customer_id_{self.item_list[i].customer_id}" in total_by_customer:
        #        total_by_customer[f"customer_id_{self.item_list[i].customer_id}"]["total_by_user"] += self.item_list[i].total
        #     else:
        #        total_by_customer[f"customer_id_{self.item_list[i].customer_id}"] = {
        #         "total_by_user" : self.item_list[i].total
        #        }
        for item in self.item_list:
            if f"customer_id_{item.customer_id}" in total_by_customer:
               total_by_customer[f"customer_id_{item.customer_id}"]["total_by_user"] += item.total
            else:
               total_by_customer[f"customer_id_{item.customer_id}"] = {
                "total_by_user" : item.total
               }                
        return total_by_customer


if __name__ == "__main__":
    invoice = Invoice()
    # invoice.add_items([LineItem(1,-1,3.5)])
    invoice.add_items([LineItem(1,2,3.5), LineItem(1,2,5.5), LineItem(3,2,3.5), LineItem(2,2,5.5), LineItem(3,2,3.5), LineItem(5,2,5.5)])

    # print(invoice.total_by_customer())
