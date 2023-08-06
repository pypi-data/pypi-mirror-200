"""Module for interacting with FreeAgent company data."""
from freeagent_api.base_object import BaseObject


class Company(BaseObject):
    """Representation of a company.

    See https://dev.freeagent.com/docs/company
    """

    API_FIELDS = [
        "url",
        "id:integer",
        "name",
        "subdomain",
        "type",
        "currency",
        "mileage_units",
        "company_start_date:date",
        "trading_start_date:date",
        "first_accounting_year_end:date",
        "freeagent_start_date:date",
        "address1",
        "address2",
        "address3",
        "town",
        "region",
        "postcode",
        "country",
        "company_registration_number",
        "contact_email",
        "contact_phone",
        "website",
        "business_type",
        "business_category",
        "short_date_format",
        "sales_tax_name",
        "sales_tax_registration_number",
        "sales_tax_effective_date:date",
        "sales_tax_rates",
        "sales_tax_is_value_added:boolean",
        "cis_enabled:boolean",
        "locked_attributes",
        "created_at:datetime",
        "updated_at:datetime",
        "vat_first_return_period_ends_on:date",
        "initial_vat_basis",
        "initially_on_frs:boolean",
        "initial_vat_frs_type",
        "sales_tax_deregistration_effective_date:date",
        "second_sales_tax_name",
        "second_sales_tax_rates",
        "second_sales_tax_is_compound:boolean",
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


    def address(self, include_country: bool = True) -> str:
        """Get the company's address as a multiline string.

        Args:
            include_country (bool, optional): Whether to include the country in
                the returned string. Defaults to True.

        Returns:
            str: Full company address.
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
