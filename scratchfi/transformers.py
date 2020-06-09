from scratchfi.services import create_account


class Transformer:
    def __init__(self, query_str):
        self.query_str = query_str


class AccountTransformer(Transformer):
    def __init__(self, query_str):
        super().__init__(query_str)

    def get_accounts(self):
        return self.query_str.getlist('accountId')

