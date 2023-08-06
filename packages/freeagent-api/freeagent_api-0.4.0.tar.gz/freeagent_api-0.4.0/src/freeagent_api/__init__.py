"""Python module for interacting with the FreeAgent accounting software API.

Currently limited to invoice related stuff.
"""
from datetime import datetime
from time import sleep
import logging
import requests

from freeagent_api.oauth import OAuthHandler

from freeagent_api.bank_account import BankAccount
from freeagent_api.company import Company
from freeagent_api.contact import Contact
from freeagent_api.invoice import Invoice
from freeagent_api.invoice_item import InvoiceItem
from freeagent_api.project import Project
from freeagent_api.user import User
from freeagent_api.accounting_category import AccountingCategory


SANDBOX_API_BASE = 'https://api.sandbox.freeagent.com/v2'
PRODUCTION_API_BASE = 'https://api.freeagent.com/v2'

# Maximum number of attempts to contact the API if rate limiting occurs
MAX_RETRIES = 5


class ApiClient:
    """Main API client class.

    This is the main API for interacting with the FreeAgent API. it's currently
    limited to obtaining invoices and related data. Note that you will need to
    call do_auth() or load a serialised authentication token into the
    serialised_token attribute for API calls to work. All data returned will be
    from the authenticated user's account.

    Rate limiting will be handled automatically if too many requests are made in
    a short time (see https://dev.freeagent.com/docs/introduction for the
    limits) by waiting as advised by the API.
    """

    def __init__(self, client_id: str, client_secret: str, use_sandbox: bool = False):
        """Initialise the instance.

        Args:
            client_id (str): Client ID for your app.
            client_secret (str): Client secret for your app.
            use_sandbox (bool, optional): Whether to use the sandbox or production system. Defaults
                to False, meaning to use the production system.
        """
        self.use_sandbox = use_sandbox

        if use_sandbox:
            self.api_base = SANDBOX_API_BASE
        else:
            self.api_base = PRODUCTION_API_BASE

        self.logger = logging.getLogger(__name__)
        self.oauth = OAuthHandler(client_id, client_secret, use_sandbox)


    def do_auth(self, only_listen_on_localhost: bool = True):
        """Get an authentication token for the users's account.

        Just a pass-through function to the OAuthHandler instance.
        """
        self.oauth.do_auth(only_listen_on_localhost=only_listen_on_localhost)


    @property
    def serialised_token(self) -> str:
        """Serialise the authentications for storage.

        Just a pass-through function to the OAuthHandler instance.

        Returns:
            str: storable tokens
        """
        return self.oauth.serialised_token

    @serialised_token.setter
    def serialised_token(self, value: str):
        self.oauth.serialised_token = value


    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Wrapper around requests.get.

        Args:
            endpoint (str): API endpoint to access. Note: Base url of
                'https://api.(sandbox.)freeagent.com/v2' will be added
                automatically.

        Returns:
            dict: Request response as decoded JSON object
        """
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint

        #print("GET", self.api_base + endpoint, "with params", params)

        self.oauth.update_tokens()
        response = None
        retries = MAX_RETRIES
        while retries > 0:
            response = requests.get(
                self.api_base + endpoint,
                headers = { "Authorization": self.oauth.authorisation_header },
                timeout = 10,
                params = params,
            )

            if 'retry-after' in response.headers:
                self.logger.info(
                    "Hit API rate limit, waiting %s seconds before retrying",
                    response.headers['Retry-After'],
                )
                retries -= 1
                if retries > 0:
                    sleep(int(response.headers['retry-after']))
                else:
                    raise RuntimeError(f"Failed to get API response after {MAX_RETRIES} retries due to rate limiting")

            else:
                break

        #TODO: Parse 'Link' header to get additional pages of results
        #if 'link' in response.headers and response.headers['link'] != "":
        #    print("link:", response.headers['Link'])

        return response.json()


    def get_company(self) -> Company:
        """Get information about the company.

        Returns:
            Company: Company data.
        """
        data = self._get('/company')['company']
        if self.use_sandbox:
            data['subdomain'] += ".sandbox"
        return Company(data)


    def get_user(self) -> User:
        """Get information about the currently authorised user.

        Returns:
            freeagent.User: User data.
        """
        data = self._get('/users/me')['user']
        return User(data)


    def get_contact(self, contact_id: int) -> Contact:
        """Get information about a contact.

        Args:
            contact_id (int): ID of the contact. Typically obtained from the
                contact field of a freeagent.Invoice object or similar.

        Returns:
            Contact: Contact data.
        """
        data = self._get(f'/contacts/{int(contact_id)}')
        return Contact(data.get('contact'))


    def get_invoices(self,
        status: str = "all",
        within_months: int = None,
        updated_since: datetime = None,
        sort_order: str = "created_at"
    ) -> list[Invoice]:
        """Get a list of invoices with their associated data.

        All invoices will automatically have their line item data included.

        Args:
            status (str, optional): Status of invoices to get. Valid values are:
                - all: Show all invoices.
                - recent_open_or_overdue: Show only recent, open, or overdue invoices.
                - open: Show only open invoices.
                - overdue: Show only overdue invoices.
                - open_or_overdue: Show only open or overdue invoices.
                - draft: Show only draft invoices.
                - paid: Show only paid invoices.
                - scheduled_to_email: Show only invoices scheduled to email.
                - thank_you_emails: Show only invoices with active thank you emails.
                - reminder_emails: Show only invoices with active reminders.
                - last_N_months: Show only invoices from the last N months.
                Defaults to "all". Cannot be specified at the same time as 'within_months'.
            within_months (int, optional): Maximum age of the invoice in months. Cannot be specified
                at the same time as 'status'. Defaults to None.
            updated_since (datetime, optional): Only return invoices updated since this timestamp.
                Defaults to None, meaning no limit.
            sort_order (str, optional): Order to return results in. Valid values are:
                - created_at: Sort by the time the invoice was created.
                - updated_at: Sort by the time the invoice was last modified.
                Defaults to "created_at".

        Returns:
            list[Invoice]: List of invoices.
        """
        if status not in ["all", "recent_open_or_overdue", "open", "overdue",
                          "open_or_overdue", "draft", "paid", "scheduled_to_email",
                          "thank_you_emails", "reminder_emails"]:
            raise ValueError("Invalid status for invoice request")
        if within_months is not None and status != "all":
            raise ValueError("Cannot specify both status and within_months for getting invoices")
        if sort_order not in ["created_at", "updated_at", "-created_at", "-updated_at"]:
            raise ValueError("Invalid sort order for invoice request")

        request_params = {
            'nested_invoice_items': True,
            'sort': sort_order,
        }
        if updated_since is not None:
            request_params['updated_since'] = updated_since.isoformat()

        if within_months is not None:
            request_params['view'] = f"last_{within_months}_months"
        else:
            request_params['view'] = status

        data = self._get('/invoices', request_params)

        invoices = []
        for data_invoice in data.get('invoices'):
            invoice = Invoice(data_invoice)
            invoices.append(invoice)

        return invoices


    def get_invoice(self, invoice_id: int) -> Invoice:
        """Get a specified invoice from its ID.

        The invoice will automatically have its line item data included.

        invoice_id (int): ID of invoice to retrieve.

        Returns:
            Invoice: Invoice data object.
        """
        data = self._get(f"/invoices/{invoice_id}")

        invoice = Invoice(data.get('invoice'))
        return invoice


    def get_bank_account(self, account_id: int) -> BankAccount:
        """Get bank account data.

        Args:
            account_id (int): ID of the account. Typically obtained from the
                bank_account field of a freeagent.Invoice object or similar.

        Returns:
            BankAccount: Bank account data object.
        """
        data = self._get(f'/bank_accounts/{int(account_id)}')
        return BankAccount(data.get('bank_account'))


    def get_project(self, project_id: int) -> Project:
        """Get project data.

        Args:
            project_id (int): ID of the project. Typically obtained from the
                project field of a freeagent.Invoice object or similar.

        Returns:
            Project: Project data object.
        """
        data = self._get(f'/projects/{int(project_id)}')
        return Project(data.get('project'))


    def get_accounting_category(self, category_id: str) -> AccountingCategory:
        """Get an accounting category's data.

        Args:
            category_id (str): ID of the category. Typically obtained from the
                category field of a freeagent.InvoiceItem object or similar.

        Returns:
            AccountingCategory: Category data object.
        """
        data = self._get(f'/categories/{category_id}')
        return AccountingCategory(data.get('income_categories'))
