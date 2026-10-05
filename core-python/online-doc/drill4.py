class Idempotency:
    def __init__(self, event_id:str, seen:set[str] | None = None):
        # self.seen = seen if seen is not None else set().      (if you don't to share when nothing is passed)
        self.seen = seen #this means shared becasue in main you pass same seen object whihc points t same memoery form all three instances san dis jsut being udated here in that same memeory refrence
        # self.seen = set(seen) # this means crea new set so nothing gets shared here
        self.event_id = event_id


    def process_event(self):
        if self.event_id in self.seen:
            print("skipped")
        else:
            self.seen.add(self.event_id)
            print("created")

if __name__== "__main__":
    seen = set()
    obj = Idempotency("evt-1", seen)
    obj.process_event()
    obj2 = Idempotency("evt-1", seen)
    obj2.process_event()
    obj3 = Idempotency("evt-2", seen)
    obj3.process_event()
