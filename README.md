# wallet
Module for creating customers, transferring money between customers, getting information about customers

Initional script for creating table in database:

CREATE TABLE "customers" (
	"account_number"	INTEGER UNIQUE,
	"name_customer"	TEXT,
	"currency"	INTEGER,
	"limit_balance"	INTEGER,
	"balance"	INTEGER,
	PRIMARY KEY("account_number")
)

Actions for customer module:

add_customer    Add customer to database. Insert name and limit for
                current user
transfer_money  Insert sender name and recipient name for trasfer
                money between customers
get_customers   Insert number for get string collection
                Insert 0 for unlimited string collection

