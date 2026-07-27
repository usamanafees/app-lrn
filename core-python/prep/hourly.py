from datetime import datetime, timedelta
import json

class HourlyUsage:
    def __init__(self, timestamp:datetime, kwh:int, rate:float):
        if kwh < 0 or rate < 0:
            raise ValueError(f"kwh and rate should not be negative")
        if not isinstance(timestamp, datetime):
            raise ValueError(f"incorrect timestamp format")
        self.timestamp = timestamp
        self.kwh = kwh
        self.rate = rate

    @property
    def hour(self)-> int:
        return self.timestamp.hour

    @property
    def total(self)-> float:
        return self.kwh * self.rate


def build_reading_windows(start_timestamp:datetime, end_timestamp:datetime) -> list[tuple]:
    current_inc = start_timestamp
    timelist:list[tuple] = []
    while (current_inc + timedelta(minutes=30)) < end_timestamp:
        timelist.append((current_inc, current_inc + timedelta(minutes=30)))
        # timelist.append((f"{current_inc.hour}:{current_inc.minute}", f"{(current_inc + timedelta(minutes=30)).hour}:{(current_inc + timedelta(minutes=30)).minute}"))
        current_inc = current_inc + timedelta(minutes=30)
    timelist.append((current_inc, end_timestamp))
    return timelist

def load_rates(path="prep/rates.json") -> dict:
    with open(path, "r") as f:
        hourly_rate_mappings = { int(key): value for key, value in json.load(f)["rates_by_hour"].items() if isinstance(key, str|float)}
    return hourly_rate_mappings

def cost_for_window(window_start:datetime, window_end:datetime, kwh, rates_by_hour) -> float:
    start_hour = window_start.hour
    end_hour = window_end.hour
    if start_hour == end_hour:
        hour_rate = rates_by_hour.get(int(start_hour))
        return hour_rate * kwh
    if start_hour != end_hour:
        start_minutes = 60 - window_start.minute
        end_minutes = window_end.minute
        start_rate = rates_by_hour.get(int(start_hour))
        end_rate = rates_by_hour.get(int(end_hour))
        total_cost = (start_rate * (kwh * (start_minutes/(start_minutes+end_minutes))) + end_rate *(kwh * (end_minutes/(start_minutes+end_minutes))))
        return total_cost

def cost_for_hourly_usage(hourly_usage:list[HourlyUsage], rates_by_hour:dict) -> float:
    total_cost = 0
    for usage in hourly_usage:
        total_cost += cost_for_window(usage.timestamp, usage.timestamp + timedelta(hours=1), usage.kwh, rates_by_hour)
    return total_cost

def calculate_total_bill(start_time:datetime, end_time:datetime, kwh_readings) -> float:
    print(start_time, end_time)
    horly_rates = load_rates()
    total_cost = 0
    for index, (start, end) in enumerate(build_reading_windows(start_time, end_time)):
        total_cost += cost_for_window(start, end, kwh_readings[index], horly_rates)
    return total_cost
    

if __name__ == "__main__":
    hourly_usage = HourlyUsage(datetime.now(), 10, 0.15)
    hourly_usage1 = HourlyUsage(datetime(2026, 8, 12, 12, 5), 10, 0.15)

    # windows = build_reading_windows(datetime.now(), datetime.now() + timedelta(hours=2, minutes=21))
    # windows = build_reading_windows(datetime(2026, 7, 21, 10, 25), datetime(2026, 7, 21, 12, 32))

    # print(windows)
    # hourly_rates = load_rates()

    # print(cost_for_window(windows[0][0], windows[0][1], 3, hourly_rates))
    print("total", calculate_total_bill(datetime(2026, 7, 21, 10, 25), datetime(2026, 7, 21, 12, 32), [2, 4, 3, 2, 0.5]))

    # thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
    # print(thistuple[-1:5], "aaa")
