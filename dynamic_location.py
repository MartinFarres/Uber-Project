
class DynamicLoc:
    def __init__(self, name, direction, price):
        self.name = name
        self.direction = direction
        self.price = price

    def __repr__(self) -> str:
        return f"DynamicLoc({self.name}, {self.direction}, {self.price})"