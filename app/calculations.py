
def add(num1: int, num2: int) -> int:
    """Add two numbers together. """
    return num1 + num2


def subtract(num1: int, num2: int) -> int:
    """Subtract two numbers. """
    return num1 - num2

def multiply(num1: int, num2: int) -> int:
    """Multiply two numbers. """
    return num1 * num2

def divide(num1: int, num2: int) -> int:
    """Divide two numbers. """
    if num2 == 0:
        raise ValueError("Cannot divide by zero.")
    return num1 / num2


class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds in the bank account. """
    pass


class Bankacount:
    """A simple bank account class. """
    def __init__(self, balance: int = 0):
        self.balance = balance

    def deposit(self, amount: int) -> None:
        """Deposit money into the account. """
        self.balance += amount
    
    def withdraw(self, amount: int) -> None:
        """Withdraw money from the account. """
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds in the account.")
        self.balance -= amount
    
    def collecting_interest(self):
        """Apply interest to the account. """
        self.balance *= 1.1 
