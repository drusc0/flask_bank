from scratchfi import db
from scratchfi.constants import DEPOSIT_COMMAND, ACCOUNT_ID_FIELD, FROM_ID_FIELD, WITHDRAW_COMMAND, XFER_COMMAND, \
    FREEZE_COMMAND, THAW_COMMAND

from scratchfi.models import AccountModel, TransactionModel

COMMAND_MAPPING = {
    DEPOSIT_COMMAND: ACCOUNT_ID_FIELD,
    WITHDRAW_COMMAND: ACCOUNT_ID_FIELD,
    XFER_COMMAND: FROM_ID_FIELD,
    FREEZE_COMMAND: ACCOUNT_ID_FIELD,
    THAW_COMMAND: ACCOUNT_ID_FIELD
}


#####################
# Create
#####################
def create_account(account):
    new_account = AccountModel(account)
    try:
        db.session.add(new_account)
        db.session.commit()

        return new_account
    except Exception as e:
        print("Unable to create account: {}".format(new_account), e)
        return None


def create_transaction(transaction_request):
    command = transaction_request.cmd
    account_id = getattr(transaction_request, COMMAND_MAPPING[command])
    to_id = transaction_request.toId if hasattr(transaction_request, 'toId') else None
    amount = transaction_request.amount if hasattr(transaction_request, 'amount') else None
    new_transaction = TransactionModel(command=transaction_request.cmd,
                                       account_id=account_id,
                                       to_id=to_id,
                                       amount=amount)

    print("transaction: ", new_transaction)

    try:
        db.session.add(new_transaction)
        db.session.commit()

        return new_transaction
    except Exception as e:
        print("Unable to create account: {}".format(new_transaction), e)
        return None


#####################
# Read
#####################
def get_accounts_from(accounts):
    if not accounts:
        return get_all_accounts()

    return AccountModel.query.filter(AccountModel.account_num.in_(accounts)).all()


def get_single_account(account):
    return AccountModel.query.filter_by(account_num=account).first()


def get_all_accounts():
    return AccountModel.query.all()


def get_all_transactions():
    return TransactionModel.query.all()


#####################
# Update
#####################
def update_account(account):
    acc = get_single_account(account.account_num)
    acc = account
    db.session.commit()
