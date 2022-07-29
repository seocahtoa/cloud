import pymongo
from pymongo import MongoClient
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import random
import time
from datetime import datetime

flask_app = Flask(__name__)
#flask_app = Flask(__name__, static_folder='./build', static_url_path='/')
#flask_app = Flask(__name__)
#flask_app.run(debug=True)



class Account:
    def __init__(self, ID, AccountNumber, Balance, AccountStatus):
        self.id = ID
        self.accountNumber = AccountNumber
        self.balance = Balance
        self.accountStatus = AccountStatus

class Customer:
    def __init__(self, ID, FirstName, LastName, AssociatedAccount):
        self.id = ID
        self.firstName = FirstName
        self.lastName = LastName
        self.associatedAccount = AssociatedAccount

class Transaction:
    def __init__(self, ID, Amount, TransactionType, AssociatedAccount):
        self.id = ID
        self.amount = Amount
        self.transactionType = TransactionType
        self.associatedAccount = AssociatedAccount

# OPERATIONS

def CustomerAccountDetailsToJSON(customer, account):
    return json.dumps({
        'id': account['id'],
        'account_number': account['account_number'],
        'balance': account['balance'],
        'account_status': account['account_status'],
        'first_name': customer['first_name'],
        'last_name': customer['last_name']
    })


@flask_app.route('/')
def hello_world():
    return 'Hello World'

@flask_app.route('/retrieve_details/<accountNumber>')
def retrieve_details(accountNumber):
    uri = "mongodb+srv://cluster0.nbb3w.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-2313919381921716032.pem')
    customerDB = client['bank']['customer']
    accountDB = client['bank']['account']
    
    #get account and customer as JSON from databases
    account = accountDB.find_one({'account_number': accountNumber})
    customer = customerDB.find_one({'id': account['id']})
    
    client.close()

    return CustomerAccountDetailsToJSON(customer, account)
    
@flask_app.route('/open_account/<firstName>/<lastName>')
def open_account(firstName, lastName):
    uri = "mongodb+srv://cluster0.nbb3w.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-2313919381921716032.pem')
    db = client['bank']
    databaseAccount = db['account']
    databaseCustomer = db['customer']
    newAccountNumber = idIncrement = int(time.time())
    
    attributeAccount = {
        'id': idIncrement,
        'account_number': newAccountNumber,
        'balance': 0,
        'account_status': 'open'
    }
    databaseAccount.insert_one(attributeAccount)

    attributeCustomer = {
        'id': idIncrement,
        'first_name': firstName,
        'last_name': lastName,
        'associated_account': newAccountNumber
    }
    
    databaseCustomer.insert_one(attributeCustomer)
    client.close()
    print(newAccountNumber)
    return retrieve_details(newAccountNumber)

@flask_app.route('/close_account/<accountNumber>')
def close_account(accountNumber):


    uri = "mongodb+srv://cluster0.nbb3w.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-2313919381921716032.pem')
    accountDB = client['bank']['account']

    account_filter = {'account_number': int(accountNumber)}
    updated_val = { "$set": {'account_status': 'closed'}}

    accountDB.update_one(account_filter, updated_val)

    client.close()
    return "Deleted account"

@flask_app.route('/apply_transaction/<accountNumber>/<amount>/<transactionType>')
def apply_transaction(accountNumber, amount, transactionType):
    uri = "mongodb+srv://cluster0.nbb3w.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-2313919381921716032.pem')
    accountDB = client['bank']['account']
    transactionDB = client['bank']['transaction']

    accountNumber = int(accountNumber)
    amount = float(amount)

    account = accountDB.find_one({'account_number': accountNumber})
    balance = account['balance']
    
    if transactionType == 'credit':
        balance += amount
    else:
        balance -= amount
        
    accountDB.update_one({'account_number': accountNumber}, { '$set': {'balance': balance}})

    transaction = {
        'id': int(time.time()),
        'amount': amount,
        'transaction_type': transactionType,
        'account_number': accountNumber
    }

    transactionDB.insert_one(transaction)

    client.close()
    return "transaction complete"


if __name__ == '__main__':
    flask_app.run()
    