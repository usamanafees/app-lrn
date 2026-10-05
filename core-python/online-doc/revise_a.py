import json

class Revise:
    def __init__(self, path):
        self.path = path
        ticket_list = []
        with open("path", "r") as f:
            for line in f:
                clean_line = json.loads(line)
                clean_line = clean_line.strip()
                if not clean_line:
                    continue
                else:
                    values = clean_line.split(",")
                    if len(values) < 3:
                        continue
                        


