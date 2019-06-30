"""Module for creating customers, transferring money
   between customers, getting information about customers
"""

import random
import connect
import argparse
import log


parser = argparse.ArgumentParser(usage='%(prog)s [action]',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description="""\
Module for creating and transffering money between customers
Actions:

add_customer    Add customer to database. Insert name and limit for
                current user
transfer_money  Insert sender name and recipient name for trasfer
                money between customers
get_customers   Insert number for get string collection
                Insert 0 for unlimited string collection
                                 """
                                 )
parser.add_argument('action', help='Action for module')
args = parser.parse_args()
action = args.action


class Customer():


    def __init__(self, name_customer, balance, limit=0, currency='RUB'):
        self.name_customer = name_customer
        self.currency = currency
        self.limit = limit
        self.balance = balance
        self.account_number = random.randint(1000000,9999999)


    def get_customer_info(self):
        """Get information about new created customer"""
        return (f'\nCustomer created:\n'
                f'Customer name: {self.name_customer}\n'
                f'Customer currency: {self.currency}\n'
                f'Current balance: {self.balance}\n'
                f'Current limit for customer: {self.limit}\n'
                )


    def __str__(self):
        return self.get_customer_info()


def check_var_for_balance(name, choice):
    """Check variable for balance of customer"""
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
    """Creating new customer"""
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


def operations_with_money(sender, recipient, sum):
    """Operations for transferring money and logic for check sender and recipient balance"""
    connection = connect.Database()
    connection.open_connect()
    try:
        sender_get = "SELECT account_number, balance, limit_balance from CUSTOMERS WHERE name_customer='" + sender + "'"
        recipient_get = "SELECT account_number, balance, limit_balance from CUSTOMERS WHERE " \
                        "name_customer='" + recipient + "'"
        sender_info = connection.getone(sender_get)
        recipient_info = connection.getone(recipient_get)
        recipient_limit = int(recipient_info[2])
        current_sender_balance = int(sender_info[1])
        current_recipient_balance = int(recipient_info[1])
        future_sender_balance = (current_sender_balance - int(sum))
        future_recipient_balance = (current_recipient_balance + int(sum))
        if future_sender_balance > 0:
            if future_recipient_balance < recipient_limit:
                connection.query("UPDATE CUSTOMERS set balance='" + str(future_sender_balance) + "' "
                                 "WHERE account_number='" + str(sender_info[0]) + "'")
                connection.query("UPDATE CUSTOMERS set balance='" + str(future_recipient_balance) + "' "
                                 "WHERE account_number='" + str(recipient_info[0]) + "'")
                message = f'{sender} moved {sum} RUB to {recipient} bank account'
                print(message)
                log.log(message)
            elif future_recipient_balance > recipient_limit:
                print(f'Can not move {sum} to {recipient} bank account, because limit equal {recipient_limit}')
            elif future_recipient_balance == recipient_limit:
                connection.query("UPDATE CUSTOMERS set balance='" + str(future_sender_balance) + "'"
                                 " WHERE account_number='" + str(sender_info[0]) + "'")
                connection.query("UPDATE CUSTOMERS set balance='" + str(future_recipient_balance) + "'"
                                 " WHERE account_number='" + str(recipient_info[0]) + "'")
                message = f'{sender} moved {sum} to {recipient} bank account, but limit of {recipient} exhausted'
                print(message)
                log.log(message)
        elif future_sender_balance == 0:
            connection.query("UPDATE CUSTOMERS set balance='" + str(future_sender_balance) + "'"
                             " WHERE account_number='" + str(sender_info[0]) + "'")
            connection.query("UPDATE CUSTOMERS set balance='" + str(future_recipient_balance) + "'"
                             " WHERE account_number='" + str(recipient_info[0]) + "'")
            message = f'{sender} {sum} RUB to {recipient} bank account, but his balance became equal 0'
            print(message)
            log.log(message)
        elif future_sender_balance < 0:
            message = f'{sender} can not move {sum} to {recipient} because balance will become less 0'
            print(message)
            log.log(message)
    except TypeError:
        print(f'{recipient} or {sender} customers not found in database')
    finally:
        connection.close_connect()


def transfer_money(sender, recepient, sum):
    """Check sum for transferring and redirecting to operations_with_money function"""
    if int(sum) <= 0:
        print(f'Sorry, can not perform operations with {sum} sum')
    else:
        operations_with_money(sender, recepient, sum)


def get_customers():
    """Get list with information adout customers with limit for strings"""
    connection = connect.Database()
    connection.open_connect()
    try:
        limit = int(input('How much strings do you want see? '))
        if limit == 0:
            print('Name|Balance|Limit balance')
            info = connection.get('customers', 'name_customer, balance,limit_balance')
            for string in info:
                print(str(string).strip("(,',)").replace("'","").replace(",","\t"))
        else:
            info = connection.get('customers', 'name_customer, balance,limit_balance', limit)
            print('Name|Balance|Limit balance')
            for string in info:
                print(str(string).strip("(,',)").replace("'","").replace(",","\t"))
    except ValueError:
        print('Insert can be only integer')
    finally:
        connection.close_connect()


def main():
    if  action == 'add_customer':
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
