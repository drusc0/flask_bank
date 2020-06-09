from scratchfi import db, ma


class AccountModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_num = db.Column(db.String(32), index=True, unique=True)
    balance = db.Column(db.Float)
    frozen = db.Column(db.Boolean)

    def __init__(self, account_num, balance=0.0, frozen=False):
        self.account_num = account_num
        self.balance = balance
        self.frozen = frozen


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountModel
