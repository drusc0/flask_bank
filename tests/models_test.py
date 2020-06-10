from scratchfi.models import AccountModel, TransactionModel, AccountSchema, TransactionSchema

ACCOUNT_NUM = "ACCOUNT_TEST"
FROZEN = False
BALANCE = 1.50
BALANCE_0 = 0.0
COMMAND_TEST = "COMMAND_TEST"
ACCOUNT_MODEL_TEST = AccountModel(account_num=ACCOUNT_NUM, balance=BALANCE, frozen=FROZEN)
TRANSACTION_MODEL_TEST = TransactionModel(command=COMMAND_TEST, account_id=ACCOUNT_NUM)


def test_new_account():
    new_account = AccountModel(account_num=ACCOUNT_NUM, balance=BALANCE, frozen=FROZEN)
    assert (new_account.account_num == ACCOUNT_NUM)
    assert (new_account.frozen == FROZEN)
    assert (new_account.balance == BALANCE)


def test_new_account_with_defaults():
    new_account = AccountModel(account_num=ACCOUNT_NUM)
    assert (new_account.account_num == ACCOUNT_NUM)
    assert (new_account.frozen == FROZEN)
    assert (new_account.balance == BALANCE_0)


def test_new_transaction():
    new_transaction = TransactionModel(command=COMMAND_TEST, account_id=ACCOUNT_NUM)
    assert (new_transaction.account_id == ACCOUNT_NUM)
    assert (new_transaction.command == COMMAND_TEST)
    assert (new_transaction.to_id == new_transaction.amount is None)
