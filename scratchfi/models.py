from scratchfi import db, ma

from datetime import datetime

from scratchfi.constants import ACCOUNTS_TABLE_NAME, TRANSACTIONS_TABLE_NAME


class AccountModel(db.Model):
    __tablename__ = ACCOUNTS_TABLE_NAME

    id = db.Column(db.Integer, primary_key=True)
    account_num = db.Column(db.String(32), index=True, unique=True)
    balance = db.Column(db.Float)
    frozen = db.Column(db.Boolean)
    transactions = db.relationship('TransactionModel', backref='accounts', lazy=True)

    def __init__(self, account_num, balance=0.0, frozen=False):
        self.account_num = account_num
        self.balance = balance
        self.frozen = frozen

    def __repr__(self):
        return "<Account {}: ${} isFrozen: {}>".format(self.account_num, self.balance, self.frozen)


class TransactionModel(db.Model):
    __tablename__ = TRANSACTIONS_TABLE_NAME

    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(16))
    account_id = db.Column(db.String(32), db.ForeignKey('accounts.account_num'), index=True)
    to_id = db.Column(db.String(32))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, command, account_id, to_id=None, amount=None):
        self.command = command
        self.account_id = account_id
        self.to_id = to_id
        self.amount = amount

    def __repr__(self):
        return "<Transaction {} from acct id: {}>".format(self.command, self.account_id)


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountModel
        exclude = ('id',)


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TransactionModel
        include_fk = True
        exclude = ('id',)
