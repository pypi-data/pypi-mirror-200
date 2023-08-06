"""Module for interacting with FreeAgent project data."""
from freeagent_api.base_object import BaseObject


class Project(BaseObject):
    """Representation of a project.

    See https://dev.freeagent.com/docs/projects
    """

    API_FIELDS = [
        "url",
        "contact:id",
        "name",
        "status",
        "contract_po_reference",
        "uses_project_invoice_sequence:boolean",
        "currency",
        "budget:decimal",
        "budget_units",
        "hours_per_day:decimal",
        "normal_billing_rate:decimal",
        "billing_period",
        "is_ir35:boolean",
        "starts_on:date",
        "ends_on:date",
        "include_unbilled_time_in_profitability:boolean",
        "created_at:datetime",
        "updated_at:datetime",
    ]
