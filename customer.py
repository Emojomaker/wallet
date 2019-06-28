import random
import connect
import sys

action = sys.argv[1]

class Customer():


    def __init__(self, name_customer, limit=0, currency='RUB', balance=0):
        self.name_customer = name_customer
        self.currency = currency
        self.limit = limit
        self.balance = balance
        self.account_number = random.randint(1000000,9999999)


    @classmethod
    def add_customer(cls):
        return cls(
            input('Name of customer: '),
            input('Limit for customer: '),
        )


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
        return (f'Customer name: {self.name_customer}\n'
                f'Customer currency: {self.currency}\n'
                f'Current balance: {self.balance}\n'
                f'Current limit for customer: {self.limit}\n'
                )


    def __str__(self):
        return self.get_customer_info()


def transfer_money(sender, recepient, sum):
    connection = connect.Database()
    connection.open_connect()
    sender_get = "SELECT account_number, balance, limit_balance from CUSTOMERS WHERE name_customer='"+sender+"'"
    recepient_get = "SELECT account_number, balance, limit_balance from CUSTOMERS WHERE name_customer='"+recepient+"'"
    sender_info = connection.getone(sender_get)
    recepient_info = connection.getone(recepient_get)
    sender_balance = (int(sender_info[1]) - int(sum))
    recepient_balance = (int(recepient_info[1] + int(sum)))
    if (int(sender_info[1]) - int(sum)) > 0:
        if (int(recepient_info[1]) + int(sum)) < int(recepient_info[2]):
            connection.query("UPDATE CUSTOMERS set balance='"+str(sender_balance)+"' WHERE account_number='"+str(sender_info[0])+"'")
            connection.query("UPDATE CUSTOMERS set balance='"+str(recepient_balance)+"' WHERE account_number='"+str(recepient_info[0])+"'")
            print(f'{sender} moved {sum} RUB to {recepient} bank account')
    elif int(recepient_info[1] + int(sum)) >= int(recepient_info[2]):
        print(f'Can not move {sum} to {recepient} bank account')
    elif (int(sender_info[1]) - int(sum)) == 0:
        connection.query("UPDATE CUSTOMERS set balance='" + str(sender_balance) + "' WHERE account_number='" + str(
            sender_info[0]) + "'")
        connection.query("UPDATE CUSTOMERS set balance='" + str(recepient_balance) + "' WHERE account_number='" + str(
            recepient_info[0]) + "'")
        print(f'{sender} {sum} RUB to {recepient} bank account, but his balance become zero')
    connection.close_connect()


def main():
    """
    add_customer
    get_customer_info
    get_customers
    transfer_money
    """
    if action == 'add_customer':
        name = input('Name of customer: ')
        limit = input('Limit for customer: ')
        user = Customer(name, limit)
        print('\nCustomer created:')
        print(user.get_customer_info())
        connection = connect.Database()
        connection.open_connect()
        connection.query("INSERT INTO CUSTOMERS VALUES ('"+str(user.account_number)+"',"
                        "'"+str(user.name_customer)+"','"+str(user.currency)+"'"
                        ",'"+str(user.limit)+"','"+str(user.balance)+"')")
        connection.close_connect()

    elif action == 'transfer_money':
        sender = input('Name of sender: ')
        recepient = input('Name of recepient: ')
        sum = input('Sum for transfer: ')
        transfer_money(sender, recepient, sum)
    elif action == 'get_customers':
        pass


if __name__ == '__main__':
    main()
