from scratchfi.modelrequests import TransactionRequest
from scratchfi.services import create_account, create_transaction, get_single_account, get_all_accounts, \
    get_accounts_from, get_all_transactions


def test_create_account(test_client, init_db):
    acc = create_account("test_account")
    assert (acc.account_num == "test_account")


def test_create_transaction(test_client, init_db):
    trans_request = TransactionRequest({'cmd': 'DEPOSIT', 'accountId': 'test_account', 'amount': 20.0})
    transaction = create_transaction(trans_request)
    assert (transaction.account_id == 'test_account')
    assert (transaction.command == 'DEPOSIT')


def test_get_single_account(test_client, init_db):
    # from fixture, only one account added
    acc = get_single_account('account_test')
    assert (acc.account_num == 'account_test')


def test_get_all_accounts(test_client, init_db):
    # one test account from fixture and one from the create test
    accs = get_all_accounts()
    assert (len(accs) == 2)
    assert (accs[0].account_num == 'account_test')
    assert (accs[1].account_num == 'test_account')


def test_get_accounts_from():
    acc = get_accounts_from(['test_account'])
    assert (len(acc) == 1)
    assert (not acc[0].frozen)
    assert (acc[0].balance == 0.0)


def test_get_all_transactions():
    transactions = get_all_transactions()
    assert (len(transactions) == 1)
    assert (transactions[0].command == 'DEPOSIT')
