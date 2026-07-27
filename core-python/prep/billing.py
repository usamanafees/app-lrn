class LineItem:
    def __init__(self, customer_id:int, kwh:int, rate:float):
        if kwh < 0 or rate < 0:
            raise ValueError(f"kwh and rate mut be greater then 0 currenlt the kwh is {kwh} and rate is {rate}")

        self.customer_id = customer_id
        self.kwh = kwh
        self.rate = rate
        
    @property
    def total(self) -> float:
        return self.kwh * self.rate




# obj1 = LineItem(1,2,5.5)
# obj2 = LineItem(1,3,5.5)
# print(obj1.total)
# print(obj2.total)