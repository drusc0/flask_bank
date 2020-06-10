from scratchfi import db
from scratchfi.constants import DEPOSIT_COMMAND, ACCOUNT_ID_FIELD, FROM_ID_FIELD, WITHDRAW_COMMAND, XFER_COMMAND, \
    FREEZE_COMMAND, THAW_COMMAND

from scratchfi.models import AccountModel, TransactionModel
import logging

log = logging.getLogger(__name__)

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
        log.info("created new account: {}".format(new_account))
        return new_account
    except Exception as e:
        log.error("Unable to create account: {}".format(new_account), e)
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

    try:
        db.session.add(new_transaction)
        db.session.commit()
        log.info("created new transaction: {}".format(new_transaction))
        return new_transaction
    except Exception as e:
        log.error("Unable to create account: {}".format(new_transaction), e)
        return None


#####################
# Read
#####################
def get_accounts_from(accounts):
    if not accounts:
        return get_all_accounts()
    log.info("get all accounts {}".format(accounts))
    return AccountModel.query.filter(AccountModel.account_num.in_(accounts)).all()


def get_single_account(account):
    log.info("get single account from SQLite3")
    return AccountModel.query.filter_by(account_num=account).first()


def get_all_accounts():
    log.info("get all accounts from SQLite3")
    return AccountModel.query.all()


def get_all_transactions():
    log.info("get all transactions from SQLite3")
    return TransactionModel.query.all()


#####################
# Update
#####################
def update_account(account):
    acc = get_single_account(account.account_num)
    acc = account
    db.session.commit()
    log.info("update account {} to {}".format(acc, account))
