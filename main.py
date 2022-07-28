import pymongo
from pymongo import MongoClient
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import random
import time

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
        'id': account.id,
        'account_number': customer.account_number,
        'balance': account.balance,
        'status': account.status,
        'first_name': customer.first_name,
        'last_name': customer.last_name
    })


@flask_app.route('/')
def hello_world():
    return 'Hello World'

@flask_app.route('/retrieve_details/<accountNumber>')
def retrieve_details(accountNumber):
    uri = "mongodb+srv://cluster0.nbb3w.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='/Users/sminsu/Downloads/X509-cert-2313919381921716032.pem')
    customerDB = client.bank.customer
    accountDB = client.bank.account
    
    #get account and customer as JSON from databases
    account = accountDB.find_one({'account_number': accountNumber})
    customer = customerDB.find_one({'id': account['id']})
    
    #convert JSON strings to dicts
    account = json.load(account)
    customer = json.load(customer)
    
    client.close()

    return CustomerAccountDetailsToJSON(customer, account)
    
@flask_app.route('/open_account/<firstName>/<lastName>')
def open_account(firstName, lastName):
    uri = "mongodb+srv://cluster0.nbb3w.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='/Users/sminsu/Downloads/X509-cert-2313919381921716032.pem')
    db = client['bank']
    databaseAccount = db['account']
    databaseCustomer = db['customer']
    idIncrement = 0
    # collectionAccount = databaseAccount[idIncrement]
    # collectionCustomer = databaseCustomer[idIncrement]
    newAccountNumber = int(time.gmtime())
    
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
                     tlsCertificateKeyFile='/Users/sminsu/Downloads/X509-cert-2313919381921716032.pem')
    accountDB = client.bank.account
    accountDB.update_one({'account_number': accountNumber}, { '$set': {'account_status': 'closed'}})
    client.close()
    return

@flask_app.route('/apply_transaction/<accountNumber>/<amount>/<transactionType>')
def apply_transaction(accountNumber, amount, transactionType):
    uri = "mongodb+srv://cluster0.nbb3w.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='/Users/sminsu/Downloads/X509-cert-2313919381921716032.pem')
    accountDB = client.bank.account
    transactionDB = client.bank.transaction

    account = accountDB.get_one({'account_number': accountNumber})
    balance = json.load(account).balance
    
    if transactionType == 'credit':
        balance += amount
    else:
        balance -= amount
        
    accountDB.update_one({'account_number': accountNumber}, { '$set': {'balance': balance}})

    transaction = {
        'id': 0,
        'amount': amount,
        'transaction_type': transactionType,
        'account_number': accountNumber
    }

    transactionDB.insert_one(transaction)
    # account = Account('1','12345',1000,'enabled')
    # account.balance = account.balance - amount
    client.close()
    #Save into mongoDB somehow
    return account


if __name__ == '__main__':
    flask_app.run()
    