def build_billing_report(raw_lines: list[str]) -> tuple[dict[int, float], str]:
    result_list = tuple[dict[int, float]]
    for item in raw_lines:
        cust_id, kwh, rate = item.split(',')
        print(cust_id, kwh, rate)


    


if __name__ == "__main__":
    raw_lines = [
        "1,10,0.15",
        "3,5,0.20",
        "1,2,0.15",
        "bad,line",
        "2,-1,0.10",
    ]
    build_billing_report(raw_lines)