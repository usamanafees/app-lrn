from events.services import read_events


def test_read_events():
    lines_c = read_events()
    # events = read_events()
    # pline = read_events()
    # print("aaaaaa",len(list(pline)))
    # assert len(list(lines_c)) == 3
    lines = list(lines_c)
    assert len(lines) == 3
    for i,line in enumerate(lines):
        if i == 0:
            assert line.get("customer_id") == 1
            assert line.get("kwh") == "10.50"
            assert line.get("timestamp") == "2026-01-15T10:00:00Z"
        # for key,value in line.items():
        #     print(key, value)
        assert "customer_id" in line and "kwh" in line and "timestamp" in line
        
