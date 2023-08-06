"""Module for interacting with FreeAgent invoice data."""
from freeagent_api.base_object import BaseObject


class Contact(BaseObject):
    """Representation of a contact.

    See https://dev.freeagent.com/docs/contacts
    """

    API_FIELDS = [
        "url",
        "first_name",
        "last_name",
        "organisation_name",
        "active_projects_count",
        "direct_debit_mandate_state",
        "created_at:datetime",
        "updated_at:datetime",
        "email",
        "billing_email",
        "phone_number",
        "mobile",
        "address1",
        "address2",
        "address3",
        "town",
        "region",
        "postcode",
        "country",
        "uses_contact_invoice_sequence:boolean",
        "contact_name_on_invoices:boolean",
        "charge_sales_tax",
        "sales_tax_registration_number",
        "status",
        "default_payment_terms_in_days:integer",
        "locale",
    ]


    def as_dict(self) -> dict:
        """Overridden version of the base object's as_dict method.

        Generates a dictionary representation of the API object, also including
        any methods that can be called without requiring parameters.

        Returns:
            dict: Contents of object.
        """
        obj = super().as_dict()
        obj['address'] = self.address()
        return obj


    @property
    def fullname(self) -> str:
        """Get the full name of the contact.

        Returns:
            str: Contact's name.
        """
        return ((self.first_name or "") + " " + (self.last_name or "")).strip()


    @property
    def name(self) -> str:
        """Return the name to use on invoices.

        Will return either the contact's full name or the company name,
        depending on the contact_name_on_invoices setting and which one(s) are
        defined.

        Returns:
            str: Name.
        """
        if self.contact_name_on_invoices:
            return self.fullname or self.organisation_name
        else:
            return self.organisation_name or self.fullname


    def address(self, include_country: bool = True) -> str:
        """Get the company's whole address as a multiline string.

        Returns:
            str: Company address as multiline string.
        """
        address_lines = [
            self.address1,
            self.address2,
            self.address3,
            self.town,
            self.region,
            self.country if include_country else None,
            self.postcode,
        ]
        address_lines = list(filter(lambda line: line is not None, address_lines))
        return "\n".join(address_lines)
