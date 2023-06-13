
class Direction:
    def __init__(self, edge1, d1, edge2, d2):
        self.edge1 = edge1
        self.edge2 = edge2
        self.d1 = d1
        self.d2 = d2

    def __repr__(self) -> str:
        return f"Direction(<{self.edge1}, {self.d1}>, <{self.edge2}, {self.d2}>)"