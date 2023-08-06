"""Module for interacting with FreeAgent bank account data."""
from freeagent_api.base_object import BaseObject


class BankAccount(BaseObject):
    """Representation of a bank account.

    See https://dev.freeagent.com/docs/bank_accounts
    """

    API_FIELDS = [
        "url",
        "type",
        "name",
        "currency",
        "is_personal:boolean",
        "is_primary:boolean",
        "status",
        "bank_name",
        "opening_balance:decimal",
        "bank_code",
        "current_balance:decimal",
        "latest_activity_date:date",
        "created_at:datetime",
        "updated_at:datetime",
        "bank_guess_enabled:boolean",
        "account_number",
        "sort_code",
        "secondary_sort_code",
        "iban",
        "bic",
        "account_number",
        "email",
    ]
