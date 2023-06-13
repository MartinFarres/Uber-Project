
class StaticLoc:
    def __init__(self, name, direction):
        self.name = name
        self.direction = direction

    def __repr__(self) -> str:
        return f"StaticLoc({self.name}, {self.direction})"