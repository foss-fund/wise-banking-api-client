from typing import Any

from apiron import JsonEndpoint
from munch import munchify

from wise_banking_api_client import Client
from wise_banking_api_client.base import Base


class SubscriptionService(Base):
    list = JsonEndpoint(path="/v3/profiles/{profile_id}/subscriptions")
    get = JsonEndpoint(path="/v3/profiles/{profile_id}/subscriptions/{subscription_id}")


class Subscription:
    def __init__(self, client: Client):
        self.service = SubscriptionService(client=client)

    def list(self, profile_id: str) -> Any:
        return munchify(self.service.list(profile_id=profile_id))

    def get(self, profile_id: str, subscription_id: str) -> Any:
        return munchify(self.service.get(profile_id=profile_id, subscription_id=subscription_id))
