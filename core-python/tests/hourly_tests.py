
from prep.hourly import load_rates

def test_cost_for_window():
    hourly_rates = load_rates()
    print(hourly_rates, "aaaaa")

