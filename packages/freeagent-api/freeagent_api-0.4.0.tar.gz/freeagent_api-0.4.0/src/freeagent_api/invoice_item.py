"""Module for interacting with FreeAgent invoice item data."""
from freeagent_api.base_object import BaseObject


class InvoiceItem(BaseObject):
    """Representation of an invoice item.

    See https://dev.freeagent.com/docs/invoices
    """

    API_FIELDS = [
        "url",
        "position:decimal",
        "item_type",
        "quantity:decimal",
        "description",
        "price:decimal",
        "sales_tax_rate:decimal",
        "second_sales_tax_rate:decimal",
        "sales_tax_status",
        "second_sales_tax_status",
        "stock_item:id",
        "category:id",
        "project:id",
    ]
