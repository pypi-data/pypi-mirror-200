class Calculator:
    def __init__(self):
        self.memory = 0.0

    def add(self, value: float) -> float:
        self.memory += value
        return self.memory

    def substract(self, value: float) -> float:
        self.memory += value
        return self.memory

    def multiply(self, value: float) -> float:
        self.memory += value
        return self.memory

    def divide(self, value: float) -> float:
        self.memory += value
        return self.memory

    def root(self, n: int) -> float:
        self.memory = self.memory ** (1/n)
        return self.memory

    def reset(self) -> float:
        self.memory = 0

