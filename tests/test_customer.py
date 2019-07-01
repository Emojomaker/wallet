import pytest
import customer
import connect
import unittest.mock as mock

@pytest.fixture(scope="session")
def create_connect():
    connection = connect.Database()
    connection.open_connect()
    connection.close_connect()


@pytest.mark.parametrize("name_customer, balance", [
    ('Paul',500),
    ('Sam',300),
    ('Paul', '500'),
    ('Sam', '300'),
])
def test_class_customer(name_customer,balance):
    user = customer.Customer(name_customer, balance)
    assert user.name_customer == name_customer
    assert user.balance == balance
    assert user.currency == 'RUB'
    assert user.limit == 0


@pytest.mark.parametrize("name, choice, balance", [
    ('Paul','Y', 500),
    ('Paul', 'y', 300),
    ('Sam','N', 0),
    ('Sam','n', 0),
])
def test_input_check_var_for_variables(monkeypatch, name, choice, balance):
    monkeypatch.setattr('builtins.input', lambda _: balance)
    assert customer.check_var_for_balance(name, choice) == balance


@pytest.mark.parametrize("name, limit, choice", [
    ('Paul',500, 'Y'),
    ('Paul', 500, 'y'),
    ('Sam', 300, 'n'),
    ('Sam', 200, 'N'),
])
def test_input_add_customer(monkeypatch, name, limit, choice):
    monkeypatch.setattr('builtins.input', lambda _: choice)
    assert customer.add_customer() == None


@pytest.mark.parametrize("choice", [
    (1),
    (2),
    (3),
    (0),
])
def test_get_customers(monkeypatch, choice):
    monkeypatch.setattr('builtins.input', lambda _: choice)
    assert customer.get_customers() == None


@pytest.mark.parametrize("sender, recipient, sum", [
    ('Paul', 'Sam', 100),
    ('Sam', 'Paul', 100),
    ('Paul', 'Kata', 200),
    ('Kata','Paul', 200),
])
def test_transfer_money(sender, recipient, sum):
    assert customer.transfer_money(sender, recipient, sum) == None









