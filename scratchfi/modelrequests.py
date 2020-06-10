from scratchfi.constants import ACCOUNT_ID_FIELD


class TransactionRequest:
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])


class AccountRequest:
    def __init__(self, account_num):
        setattr(self, ACCOUNT_ID_FIELD, account_num)
