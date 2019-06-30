import pytest
import customer
import connect
import unittest.mock as mock


def test_customer():
    users = ['Sam', 'Jack', 'Andrew', 'Kate']
    balances = [100, 300, '500', '-1']
    for user,balance in zip(users,balances):
        custom = customer.Customer(user, balance)
        assert custom.name_customer == user
        assert custom.balance == balance


def test_no_value():
    with pytest.raises(Exception) as info:
        obj = customer.Customer()


@pytest.yield_fixture
def fake_input():
    with mock.patch('customer.check_var_for_balance') as mod:
        yield mod


def test_check_var_for_balanse(fake_input):
    choises = ['y','Y','n','N']
    names = ['Pauls', 'Jeni', 'Rodger']
    for ch, name in zip(choises, names):
        fake_input.return_value = '500'
        customer.check_var_for_balance(ch, name)


def test_get_customers():
    with mock.patch('customer.get_customers', return_value=0):
        assert customer.get_customers() == 0
    with mock.patch('customer.get_customers', return_value=5):
        assert customer.get_customers() == 5









