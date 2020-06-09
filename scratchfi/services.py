from scratchfi import db

from scratchfi.models import AccountModel, TransactionModel


def create_account(account):
    new_account = AccountModel(account)
    try:
        db.session.add(new_account)
        db.session.commit()

        return new_account
    except Exception as e:
        raise Exception("Unable to create account: {}".format(new_account), e)


def get_accounts_from(accounts):
    if not accounts:
        return get_all_accounts()

    return AccountModel.query.filter(AccountModel.account_num.in_(accounts)).all()


def get_all_accounts():
    return AccountModel.query.all()


def get_all_transactions():
    return TransactionModel.query.all()
