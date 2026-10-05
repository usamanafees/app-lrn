import json


class Drill:
    def __init__(self, path:str):
        self.path = path
    
    def filter_lines(self) -> dict[list]:
        objArr=[]
        seen=set()
        objArrErrorList:list[dict] =[]
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                    # (objArr if item.get("text") else objArrErrorList).append(item)
                    if item.get("text") and item.get("id") and item.get("section") and item["id"] not in seen:
                        # and all(("id", item["id"]) not in req.items() for req in objArr):
                        #   
                            objArr.append(item)
                            seen.add(item["id"])  
                    else:
                        objArrErrorList.append(item)
                except Exception as e:
                    print(line, type(e).__name__, e)
                    continue
        return {"ValidateList":objArr, "ErrorList":objArrErrorList}

if __name__ == "__main__":
    drill = Drill("records.jsonl")
    results:dict[list] = drill.filter_lines()
    for key,value in results.items():
        if "ValidateList" == key:
            print("ValidateList")
            for i in range(len(value)):
                print(value[i])
        else:
            print("errors")
            for i in range(len(value)):
                print(value[i])