import pytest
from app.calculations import add, subtract, multiply, divide, Bankacount, InsufficientFundsError


@pytest.fixture
def zero_bank_account():
    """Fixture for a bank account with zero balance. """
    return Bankacount()

@pytest.fixture
def bank_account():
    """Fixture for a bank account with a balance of 100. """
    return Bankacount(100)


@pytest.mark.parametrize("num1, num2, expected", [
    (1, 3, 4),
    (5, 2, 7),
    (4, 4, 8),
    (10, 2, 12)
])
def test_addZ(num1, num2, expected):
    """Test the add function. """
    assert add(num1, num2) == expected


def test_subtract():
    """Test the subtract function. """
    assert subtract(5, 2) == 3

def test_multiply():
    """Test the multiply function. """
    assert multiply(4, 3) == 12

def test_divide():
    """Test the divide function. """
    assert divide(10, 2) == 5

def test_bank_set_initial_balance(bank_account):
    """Test setting the initial balance of the bank account. """
    assert bank_account.balance == 100

def test_default_initial_balance(zero_bank_account):
    """Test the default initial balance of the bank account. """
    assert zero_bank_account.balance == 0

def test_deposit(bank_account):
    """Test depositing money into the bank account. """
    bank_account.deposit(50)
    assert bank_account.balance == 150

def test_withdraw(bank_account):
    """Test withdrawing money from the bank account. """
    bank_account.withdraw(30)
    assert bank_account.balance == 70


def test_collecting_interest(bank_account):
    """Test collecting interest on the bank account. """
    bank_account.collecting_interest()
    assert round(bank_account.balance) == 110



@pytest.mark.parametrize("deposit_amount, withdraw_amount, expected_balance", [
    (100, 30, 70),
    (200, 50, 150),
    (150, 20, 130),
    (300, 100, 200)
])
def test_banking_transaction(zero_bank_account, deposit_amount, withdraw_amount, expected_balance):
    """Test a series of banking transactions. """
    zero_bank_account.deposit(deposit_amount)
    zero_bank_account.withdraw(withdraw_amount)
    assert round(zero_bank_account.balance) == expected_balance


def test_insufficient_funds(zero_bank_account):
    """Test withdrawing more money than the balance. """
    with pytest.raises(InsufficientFundsError):
        zero_bank_account.withdraw(50)