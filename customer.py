import random
import connect
import argparse
import sys
action = sys.argv[1]

class Customer():


    def __init__(self, name_customer, balance, limit=0, currency='RUB'):
        self.name_customer = name_customer
        self.currency = currency
        self.limit = limit
        self.balance = balance
        self.account_number = random.randint(1000000,9999999)


    def data_of_customer(self, name_user):
        if name_user == self.name_customer:
            data = {
            'id': self.account_number,
            'name':self.name_customer,
            'balance': self.balance,
            'limit': self.limit,
            'currency': self.currency,
            }
        return data


    def get_customer_info(self):
        return (f'\nCustomer created:\n'
                f'Customer name: {self.name_customer}\n'
                f'Customer currency: {self.currency}\n'
                f'Current balance: {self.balance}\n'
                f'Current limit for customer: {self.limit}\n'
                )


    def __str__(self):
        return self.get_customer_info()


def check_var_for_balance(name, choice):
    if choice == 'y' or choice == 'Y':
        try:
            balance = int(input(f'Enter balance for {name}: '))
        except ValueError:
            print('Enter integer value')
            balance = 0
    elif choice == 'n' or choice == 'N':
        balance = 0
    return balance


def add_customer():
    name = input('Name of customer: ')
    if len(name) == 0 or len(name) < 4:
        print('Sorry, enter correct name for customer. Length must be 4 letters')
    else:
        try:
            limit = int(input('Limit for customer: '))
            connection = connect.Database()
            connection.open_connect()
            choice = input(f'Do you have change balance for {name}?(y/n) ')
            balance = check_var_for_balance(name, choice)
            user = Customer(name, balance, limit)
            if balance > limit:
                print('Balance can not be more than limit')
            else:
                print(user.get_customer_info())
                connection.query("INSERT INTO CUSTOMERS VALUES ('" + str(user.account_number) + "',"
                             "'" + str(user.name_customer) + "','" + str(user.currency) + "'"
                             ",'" + str(user.limit) + "','" + str(user.balance) + "')")
                connection.close_connect()
        except ValueError:
            print('Limit can not be string, only integer')


def operations_with_money(sender, recepient, sum):
    connection = connect.Database()
    connection.open_connect()
    try:
        sender_get = "SELECT account_number, balance, limit_balance from CUSTOMERS WHERE name_customer='" + sender + "'"
        recepient_get = "SELECT account_number, balance, limit_balance from CUSTOMERS WHERE " \
                        "name_customer='" + recepient + "'"
        sender_info = connection.getone(sender_get)
        recepient_info = connection.getone(recepient_get)
        recepient_limit = int(recepient_info[2])
        current_sender_balance = int(sender_info[1])
        current_recepient_balance = int(recepient_info[1])
        future_sender_balance = (current_sender_balance - int(sum))
        future_recepient_balance = (current_recepient_balance + int(sum))
        if future_sender_balance > 0:
            if future_recepient_balance < recepient_limit:
                connection.query("UPDATE CUSTOMERS set balance='" + str(future_sender_balance) + "' "
                                 "WHERE account_number='" + str(sender_info[0]) + "'")
                connection.query("UPDATE CUSTOMERS set balance='" + str(future_recepient_balance) + "' "
                                 "WHERE account_number='" + str(recepient_info[0]) + "'")
                print(f'{sender} moved {sum} RUB to {recepient} bank account')
            elif future_recepient_balance > recepient_limit:
                print(f'Can not move {sum} to {recepient} bank account, because limit equal {recepient_limit}')
            elif future_recepient_balance == recepient_limit:
                connection.query("UPDATE CUSTOMERS set balance='" + str(future_sender_balance) + "'"
                                 " WHERE account_number='" + str(sender_info[0]) + "'")
                connection.query("UPDATE CUSTOMERS set balance='" + str(future_recepient_balance) + "'"
                                 " WHERE account_number='" + str(recepient_info[0]) + "'")
                print(f'{sender} moved {sum} to {recepient} bank account, but limit of {recepient} exhausted')
        elif future_sender_balance == 0:
            connection.query("UPDATE CUSTOMERS set balance='" + str(future_sender_balance) + "'"
                             " WHERE account_number='" + str(sender_info[0]) + "'")
            connection.query("UPDATE CUSTOMERS set balance='" + str(future_recepient_balance) + "'"
                             " WHERE account_number='" + str(recepient_info[0]) + "'")
            print(f'{sender} {sum} RUB to {recepient} bank account, but his balance became equal 0')
        elif future_sender_balance < 0:
            print(f'{sender} can not move {sum} to {recepient} because balance will become less 0')
    except TypeError:
        print(f'{recepient} or {sender} customers not found in database')
    finally:
        connection.close_connect()


def transfer_money(sender, recepient, sum):
    if int(sum) <= 0:
        print(f'Sorry, can not perform operations with {sum} sum')
    else:
        operations_with_money(sender, recepient, sum)

def get_customers():
    connection = connect.Database()
    connection.open_connect()
    try:
        limit = int(input('How mutch strings do you want see? '))
        if limit == 0:
            info = connection.get('customers', 'name_customer, balance,limit_balance')
            for string in info:
                print(str(string).strip("(,',)").replace("'",""))
        else:
            info = connection.get('customers', 'name_customer, balance,limit_balance', limit)
            print('Name|Balance|Limit balance')
            for string in info:
                print(str(string).strip("(,',)").replace("'",""))
    except ValueError:
        print('Insert can be only integer')
    finally:
        connection.close_connect()


def main():
    if action == 'add_customer':
        add_customer()
    elif action == 'transfer_money':
        sender = input('Name of sender: ')
        recepient = input('Name of recepient: ')
        sum = input('Sum for transfer: ')
        transfer_money(sender, recepient, sum)
    elif action == 'get_customers':
        get_customers()


if __name__ == '__main__':
    main()
