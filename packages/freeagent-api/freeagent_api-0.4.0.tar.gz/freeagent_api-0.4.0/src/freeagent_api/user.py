"""Module for interacting with FreeAgent user data."""
from freeagent_api.base_object import BaseObject


class User(BaseObject):
    """Representation of a user.

    See https://dev.freeagent.com/docs/user
    """

    API_FIELDS = [
        "url",
        "email",
        "first_name",
        "last_name",
        "ni_number",
        "unique_tax_reference",
        "role",
        "opening_mileage:decimal",
        "send_invitation:boolean",
        "permission_level:integer",
        "created_at:datetime",
        "updated_at:datetime",
        "current_payroll_profile",
        "total_pay_in_previous_employment:decimal",
        "total_tax_in_previous_employment:decimal",
    ]


    @property
    def fullname(self) -> str:
        """Get the full name of the user.

        Returns:
            str: User's name.
        """
        return (self.first_name + " " + self.last_name).strip()
