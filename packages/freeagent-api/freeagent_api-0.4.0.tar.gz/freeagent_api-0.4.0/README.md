# FreeAgent API

A package for interacting with the [FreeAgent](https://freeagent.com/)
accounting software.

Mainly made for personal use, but sharing it here because... well, why not? :-)

## Limitations

Currently only invoice related functionality is available. Other features are
likely to be added in time.

## Install from PyPI

```sh
pip install freeagent_api
```

## Usage

```python
import freeagent_api

api = freeagent_api.ApiClient(
    client_id = '<client id from dev.freeagent.com>',
    client_secret = '<client secret from dev.freeagent.com>',
    use_sandbox = True,
)

# Load a serialised token from wherever you store them here
api.serialised_token = your_storage.get_token() # Implement this yourself
# or ask the user to authorise access to their account
api.do_auth()

# Get some basic info about the authenticated user
user = api.get_user()
company = api.get_company()
print(f"{user.fullname} works for {company.name}")
print()

# Find unpaid invoices
for invoice in api.get_invoices(status = "open_or_overdue"):
    print(f"Invoice {invoice.reference} for {invoice.currency} {invoice.total_value} is unpaid")

# Store the authentication token for later use
storage.set_token(api.serialised_token) # Implement this yourself
```

This will, assuming appropriate invoices exist, display something along the
lines of:

```text
Tim the Enchanter works for Arthurian Enchanters Ltd

Invoice ART01 for GBP 112.15 is unpaid
Invoice ART02 for USD 245.10 is unpaid
Invoice RBT01 for GBP 2.50 is unpaid
```

## Available data

See FreeAgent's [official API documentation](https://dev.freeagent.com/docs/)
for the basic fields in each object. In addition to those, the following
properties and methods are available:

### freeagent_api.Company

-   `address(include_country = True)` returns the full address of the authorised
    user's company as a multiline string.

### freeagent_api.Contact

-   `address(include_country = True)` returns the full address of the contact
    as a multiline string.
-   `fullname` returns the first and last name of the contact (if defined) as a
    single string.
-   `name` returns the name to use on invoices. This will either be the
    contact's full name or company name, depending on which is defined and the
    contact_name_on_invoices setting for the contact.

### freeagent_api.User

-   `fullname` returns the first and last name of the authorised user as a
    single string.
