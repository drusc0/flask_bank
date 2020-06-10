from scratchfi import app
from scratchfi.models import AccountSchema, TransactionSchema
from scratchfi.services import get_accounts_from, create_account, get_all_transactions

from flask import request, jsonify

from scratchfi.transformers import TransactionTransformer, AccountTransformer

account_schema = AccountSchema()
account_schemas = AccountSchema(many=True)
transaction_schema = TransactionSchema()
transaction_schemas = TransactionSchema(many=True)


@app.route('/')
def home():
    """Home page
    This site will host information to use this API. This will make
    it possible for the user to land on the homepage and also
    be able to quickly understand which APIs are available,
    and how they can be used.
    """

    return "Welcome to Scratch.fi mini challenge"


@app.route('/accounts', methods=['GET'])
def get_accounts():
    """Accounts endpoint
    Returns the whole list of accounts stored in the mini.db
    when there is a querystr with accountIds, we use that to filter the
    list to be returned.
    If an account that doesn't exist is requested, the account is created
    and appended to the results (balance 0 and not frozen)
    """
    response = AccountTransformer.handle(request.args)
    return jsonify(account_schemas.dump(response))


@app.route('/transactions', methods=['GET', 'POST'])
def get_transactions():
    """Transactions endpoint
    Returns a complete list of transactions performed.
    When POST method is invoked, returns transactions unable to complete
    """
    if request.method == 'POST':
        response = TransactionTransformer.handle(request.json)
        return jsonify(response)

    output = get_all_transactions()
    return jsonify(transaction_schemas.dump(output))
