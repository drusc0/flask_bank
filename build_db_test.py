from scratchfi import db
from scratchfi.models import AccountModel, TransactionModel

# Initial data
ACCOUNT = [{"accountId": "ACT100", "balance": 302.34, "frozen": False},
           {"accountId": "ACT101", "balance": 100.32, "frozen": True}]

db.create_all()
for acc in ACCOUNT:
    account = AccountModel(account_num=acc['accountId'], balance=acc['balance'], frozen=acc['frozen'])
    db.session.add(account)

db.session.commit()

TRANSACTIONS = [
    {"cmd": "DEPOSIT", "accountId": "ACT300", "amount": 100.00},
    {"cmd": "XFER", "fromId": "ACT300", "toId": "ACT100", "amount": 100.00},
    {"cmd": "FREEZE", "accountId": "ACT303"},
    {"cmd": "DEPOSIT", "accountId": "ACT303", "amount": 20.00},
    {"cmd": "WITHDRAW", "accountId": "ACT100", "amount": 5.00},
    {"cmd": "THAW", "accountId": "ACT303"}
]

for tran in TRANSACTIONS:
    t = TransactionModel(command=tran['cmd'],
                         account_id=tran['accountId'] if tran.get('accountId') else tran['fromId'],
                         to_id=tran['toId'] if tran.get('toId') else None,
                         amount=tran['amount'] if tran.get('amount') else None)
    db.session.add(t)
