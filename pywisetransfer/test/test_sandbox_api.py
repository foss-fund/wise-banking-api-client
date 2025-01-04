"""This runs tests with the sandbox API.

In order to run these tests, you need to pass a token.

pytest --api_token <token>

"""

from pywisetransfer.client import Client
from pywisetransfer.model.account import (
    LegalEntityType,
    AccountRequirement,
    RecipientAccountResponse,
    AccountRequirementType,
)
from pywisetransfer.model.currency import Currency, CurrencyCode
from pywisetransfer.model.profile import Profile, Profiles
from pywisetransfer.model.quote import ExampleQuoteRequest, QuoteResponse, QuoteStatus
from pywisetransfer.model.recipient import Recipient


def test_two_profile_types(sandbox_profiles: Profiles):
    """Check the types of profiles we have."""
    assert len(sandbox_profiles) >= 2
    assert len(sandbox_profiles.business) >= 1
    assert len(sandbox_profiles.personal) >= 1

    assert sandbox_profiles.business[0].type == "business"
    assert sandbox_profiles.personal[0].type == "personal"

    assert sandbox_profiles.business[0].is_business()
    assert sandbox_profiles.personal[0].is_personal()

    assert not sandbox_profiles.personal[0].is_business()
    assert not sandbox_profiles.business[0].is_personal()


def test_list_currencies(sandbox_currencies: list[Currency]):
    """Check the list of currencies."""
    assert len(sandbox_currencies) >= 1
    codes = [c.code for c in sandbox_currencies]
    assert "EUR" in codes
    assert "USD" in codes
    assert "GBP" in codes
    assert "AUD" in codes


def test_list_balance(sandbox_personal_balances):
    """Check the list of currencies."""
    assert len(sandbox_personal_balances) >= 1
    currencies = [b.currency for b in sandbox_personal_balances]
    assert "EUR" in currencies
    assert "USD" in currencies
    assert "GBP" in currencies
    assert "AUD" in currencies


def test_requirements(sandbox_requirements_gbp: list[AccountRequirement]):
    """Check that we can create the right requirements.

    We make sure that GBP sort code is in the requirements.
    """
    assert len(sandbox_requirements_gbp) > 0
    assert any(
        requirement.type == AccountRequirementType.sort_code
        for requirement in sandbox_requirements_gbp
    )


def test_example_quote(
    sandbox_example_quote: QuoteResponse, example_quote_request: ExampleQuoteRequest
):
    """Check that the example quote matches the request."""
    assert sandbox_example_quote.sourceCurrency == example_quote_request.sourceCurrency
    assert sandbox_example_quote.targetCurrency == example_quote_request.targetCurrency
    assert sandbox_example_quote.sourceAmount == example_quote_request.sourceAmount
    assert sandbox_example_quote.targetAmount == example_quote_request.targetAmount
    print(sandbox_example_quote.id)
    assert sandbox_example_quote.status == QuoteStatus.PENDING


def test_get_the_quote_again(
    sandbox_client: Client, sandbox_example_quote: QuoteResponse, sandbox_business_profile: Profile
):
    """Get the quote again and see if it changed."""
    quote: QuoteResponse = sandbox_client.quotes.get(
        sandbox_example_quote, sandbox_business_profile
    )
    assert quote.id == sandbox_example_quote.id


def test_email_recipient(
    sandbox_email_recipient: RecipientAccountResponse, sandbox_iban_recipient_request: Recipient
):
    """Check tha the data matches."""
    print(sandbox_email_recipient.model_dump_json(indent=4))
    assert sandbox_email_recipient.currency == CurrencyCode.EUR
    assert sandbox_email_recipient.type == AccountRequirementType.email
    assert sandbox_email_recipient.legalEntityType == LegalEntityType.PERSON
    assert sandbox_email_recipient.email == "john@doe.com"


def test_iban_recipient(
    sandbox_iban_recipient: RecipientAccountResponse, sandbox_iban_recipient_request: Recipient
):
    """Check tha the data matches."""
    assert sandbox_iban_recipient.email == "max@mustermann.de"
    assert sandbox_iban_recipient.type == AccountRequirementType.iban
    assert not sandbox_iban_recipient.ownedByCustomer
    assert sandbox_iban_recipient.currency == sandbox_iban_recipient_request.currency
