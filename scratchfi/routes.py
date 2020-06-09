from scratchfi import app
from scratchfi.models import AccountSchema, TransactionSchema
from scratchfi.services import get_accounts_from, create_account, get_all_transactions

from flask import request, jsonify

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
    accounts = request.args.getlist('accountId')
    output = get_accounts_from(accounts)

    output.extend(__create_not_present_accounts(accounts, output))

    return jsonify(account_schemas.dump(output))


@app.route('/account/<account_num>', methods=['GET'])
def get_account(account_num):
    """Account/:id endpoint
    GET method to return a single information value instead of the full list
    of accounts (like in the previous endpoints.
    """
    output = get_accounts_from(account_num)
    output.extend(__create_not_present_accounts([account_num], output))

    return account_schema.jsonify(output[0])


@app.route('/transactions', methods=['GET'])
def get_transactions():
    """Transactions endpoint
    Returns a complete list of transactions performed.
    """
    output = get_all_transactions()

    return jsonify(transaction_schemas.dump(output))


@app.route('/transactions', methods=['POST'])
def post_transactions():
    body_request = request.json

    pass


######################
# helper functions
######################
def __create_not_present_accounts(account_strings, account_models):
    if len(account_strings) != len(account_models):
        created_accounts = []
        account_set = set([x.account_num for x in account_models])
        for acc in account_strings:
            if acc not in account_set:
                try:
                    created_accounts.append(create_account(acc))
                except Exception as e:
                    print(e)
        return created_accounts
    return []
