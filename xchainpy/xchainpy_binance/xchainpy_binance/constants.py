from enum import Enum


class TransactionSide(str, Enum):
    RECEIVE = 'RECEIVE'
    SEND = 'SEND'


class TransactionType(str, Enum):
    NEW_ORDER = 'NEW_ORDER'
    ISSUE_TOKEN = 'ISSUE_TOKEN'
    BURN_TOKEN = 'BURN_TOKEN'
    LIST_TOKEN = 'LIST_TOKEN'
    CANCEL_ORDER = 'CANCEL_ORDER'
    FREEZE_TOKEN = 'FREEZE_TOKEN'
    UN_FREEZE_TOKEN = 'UN_FREEZE_TOKEN'
    TRANSFER = 'TRANSFER'
    PROPOSAL = 'PROPOSAL'
    VOTE = 'VOTE'