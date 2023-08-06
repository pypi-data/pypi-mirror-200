"""Module for interacting with FreeAgent invoice data."""
from freeagent_api.base_object import BaseObject


class AccountingCategory(BaseObject):
    """Representation of an accounting category.

    See https://dev.freeagent.com/docs/categories
    """

    API_FIELDS = [
        "url",
        "description",
        "nominal_code",
        "group_description",
        "auto_sales_tax_rate",
        "group_description",
        "allowable_for_tax:boolean",
        "tax_reporting_name",
        "auto_sales_tax_rate",
    ]
