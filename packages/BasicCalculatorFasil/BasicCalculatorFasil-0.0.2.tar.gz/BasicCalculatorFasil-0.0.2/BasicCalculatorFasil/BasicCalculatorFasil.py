from dataclasses import dataclass


@dataclass
class Calculator():
    """ Basic calculator which performs some basic arithmetic operations
        operations including: (+, -, *, /, nth root)

    Returns:
        memory of calculator after operation
    """
    memory: float = 0.0  # Define the memory attribute and initialize it to 0.0

    def add(self, number: float) -> float:
        # add number on top of the calculator memory
        self.memory += number
        return self.memory

    def subtract(self, number: float) -> float:
        # subtract number from the calculator memory
        self.memory -= number
        return self.memory

    def multiply(self, number: float) -> float:
        # multiply the calculator memory by the number
        self.memory *= number
        return self.memory

    def divide(self, number: float) -> float:
        # divide the calculator memory by the number
        self.memory /= number
        return self.memory

    def root(self, n: int) -> float:
        # compute the nth root of the calculator memory
        self.memory = self.memory ** (1.0/n)
        return self.memory

    def reset(self) -> float:
        # resets the memory to 0.0
        self.memory = 0.0
        return self.memory
