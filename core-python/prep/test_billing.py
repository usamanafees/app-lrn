from billing import LineItem   
from invoice import Invoice
from collections import defaultdict
import pytest

def test_line_item_total():
    line_item_obj = LineItem(1, 3, 5)
    assert line_item_obj.total == 15

def test_negative_values_raise_Error():
    with pytest.raises(ValueError, match="kwh and rate mut be greater then 0 currenlt the kwh is -1 and rate is 5"):
        LineItem(1, -1, 5)

    with pytest.raises(ValueError, match="kwh and rate mut be greater then 0 currenlt the kwh is 3 and rate is -5"):
        LineItem(1, 3, -5)

def test_total_by_customer():
    invoice_obj = Invoice()
    invoice_obj.add_items([LineItem(1,3,5), LineItem(1,5,5), LineItem(3,1,5)])
    # grouped_user_total = defaultdict(dict)
    # for item in invoice_obj.item_list:
    #     grouped_user_total[f"customer_id_{item.customer_id}"]["total_by_user"] += item.total
    grouped_users = invoice_obj.total_by_customer()
    assert grouped_users["customer_id_1"]["total_by_user"] == 25+15
    assert grouped_users["customer_id_3"]["total_by_user"] == 5


