from scratchfi.constants import ACCOUNT_ID_FIELD, THAW_COMMAND, FREEZE_COMMAND, DEPOSIT_COMMAND, WITHDRAW_COMMAND, \
    XFER_COMMAND, AMOUNT_FIELD, TO_ID_FIELD, FROM_ID_FIELD
from scratchfi.modelrequests import TransactionRequest, AccountRequest
from scratchfi.services import create_account, update_account, create_transaction, get_accounts_from, \
    get_single_account, get_all_transactions

import logging

log = logging.getLogger(__name__)

COMMAND_FIELDS = {
    DEPOSIT_COMMAND: {ACCOUNT_ID_FIELD, AMOUNT_FIELD},
    WITHDRAW_COMMAND: {ACCOUNT_ID_FIELD, AMOUNT_FIELD},
    XFER_COMMAND: {FROM_ID_FIELD, TO_ID_FIELD, AMOUNT_FIELD},
    FREEZE_COMMAND: {ACCOUNT_ID_FIELD},
    THAW_COMMAND: {ACCOUNT_ID_FIELD}
}


class AccountTransformer(object):
    @staticmethod
    def handle(query_str):
        accounts = query_str.getlist(ACCOUNT_ID_FIELD)
        output = get_accounts_from(accounts)
        output.extend(AccountTransformer.create_not_present_accounts(accounts, output))

        return output

    @staticmethod
    def is_account(account):
        # account does not exist, but once it is created, account is not frozen
        testing_account = get_single_account(account)
        if not testing_account:
            testing_account = AccountTransformer.create(account)

        return testing_account

    @staticmethod
    def get_account(account):
        return get_single_account(account)

    @staticmethod
    def create(account):
        return create_account(account)

    @staticmethod
    def update(account):
        return update_account(account)

    @staticmethod
    def create_not_present_accounts(account_req, account_res):
        if len(account_req) != len(account_res):
            created_accounts = []
            account_set = set([x.account_num for x in account_res])
            for acc in account_req:
                if acc not in account_set:
                    created_accounts.append(AccountTransformer.create(acc))
            return created_accounts
        return []


class TransactionTransformer(object):
    @staticmethod
    def handle(body_request=None):
        if not body_request:
            return get_all_transactions()

        unprocessed_transactions = []
        for req in body_request:
            transaction_request = TransactionRequest(req)
            transaction_accounts = TransactionTransformer.get_accounts_from_transaction_request(transaction_request)
            if TransactionTransformer.validate(transaction_request, transaction_accounts):
                TransactionTransformer.create(transaction_request)
                TransactionTransformer.update(transaction_request)
            else:
                unprocessed_transactions.append(req)

        return unprocessed_transactions

    @staticmethod
    def create(transaction):
        return create_transaction(transaction)

    @staticmethod
    def update(transaction):
        if transaction.cmd == FREEZE_COMMAND:
            account = AccountTransformer.get_account(transaction.accountId)
            account.frozen = True
            return AccountTransformer.update(account)
        elif transaction.cmd == THAW_COMMAND:
            account = AccountTransformer.get_account(transaction.accountId)
            account.frozen = False
            return AccountTransformer.update(account)
        elif transaction.cmd == DEPOSIT_COMMAND:
            account = AccountTransformer.get_account(transaction.accountId)
            account.balance += transaction.amount
            return AccountTransformer.update(account)
        elif transaction.cmd == WITHDRAW_COMMAND:
            account = AccountTransformer.get_account(transaction.accountId)
            account.balance -= transaction.amount
            return AccountTransformer.update(account)
        elif transaction.cmd == XFER_COMMAND:
            from_account = AccountTransformer.get_account(transaction.fromId)
            to_account = AccountTransformer.get_account(transaction.toId)
            from_account.balance -= transaction.amount
            to_account.balance += transaction.amount
            return [AccountTransformer.update(from_account), AccountTransformer.update(to_account)]

    @staticmethod
    def get_accounts_from_transaction_request(transaction_request):
        if transaction_request.cmd == XFER_COMMAND:
            from_account = AccountRequest(transaction_request.fromId)
            to_account = AccountRequest(transaction_request.toId)

            return [from_account, to_account]

        return [AccountRequest(transaction_request.accountId)]

    @staticmethod
    def validate(transaction_request, transaction_accounts):
        if transaction_request.cmd not in COMMAND_FIELDS:
            return False

        fields = COMMAND_FIELDS[transaction_request.cmd]
        for field in fields:
            if not hasattr(transaction_request, field):
                return False

        if transaction_request.cmd == FREEZE_COMMAND or transaction_request.cmd == THAW_COMMAND:
            AccountTransformer.is_account(transaction_accounts[0].accountId)
            return True
        elif transaction_request.cmd == DEPOSIT_COMMAND:
            account = AccountTransformer.is_account(transaction_accounts[0].accountId)
            return not account.frozen and transaction_request.amount >= 0
        elif transaction_request.cmd == WITHDRAW_COMMAND:
            account = AccountTransformer.is_account(transaction_accounts[0].accountId)
            return not account.frozen and 0 <= transaction_request.amount <= account.balance
        elif transaction_request.cmd == XFER_COMMAND:
            from_account = AccountTransformer.is_account(transaction_accounts[0].accountId)
            to_account = AccountTransformer.is_account(transaction_accounts[1].accountId)
            return not (from_account.frozen or to_account.frozen) \
                   and 0 <= transaction_request.amount <= from_account.balance
