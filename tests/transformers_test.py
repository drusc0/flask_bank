from scratchfi.modelrequests import TransactionRequest
from scratchfi.transformers import AccountTransformer, TransactionTransformer, COMMAND_FIELDS


def test_account_transformer_is_account(test_client, init_db):
    account_1 = AccountTransformer.is_account('account_test')
    account_2 = AccountTransformer.is_account('test_account')

    assert (account_1.account_num == 'account_test')
    assert (account_2.account_num == 'test_account')


def test_account_transformer_get_account(test_client, init_db):
    account = AccountTransformer.get_account('account_test')
    assert (account.account_num == 'account_test')


def test_account_transformer_create(test_client, init_db):
    account = AccountTransformer.create('new_account_test')
    assert (account.account_num == 'new_account_test')


def test_transaction_transformer_validate_not_cmd():
    transaction_request = TransactionRequest({'cmd': 'NOT_A_CMD', 'accountId': 'test_account', 'amount': 20.0})
    assert (not TransactionTransformer.validate(transaction_request, []))


def test_transaction_transformer_validate_field_not_in_cmd():
    transaction_request = TransactionRequest({'cmd': 'DEPOSIT', 'accountId': 'test_account'})
    assert (not TransactionTransformer.validate(transaction_request, []))
