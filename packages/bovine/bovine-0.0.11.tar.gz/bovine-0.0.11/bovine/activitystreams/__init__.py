from dataclasses import dataclass

from bovine.types import Visibility

from .ordered_collection_builder import OrderedCollectionBuilder
from .ordered_collection_page_builder import OrderedCollectionPageBuilder


def build_ordered_collection(url: str):
    return OrderedCollectionBuilder(url)


def build_ordered_collection_page(url: str, part_of: str):
    return OrderedCollectionPageBuilder(url, part_of)


@dataclass
class Actor:
    """Actor class represents the basic ActivityStreams actor."""

    id: str
    type: str = "Person"
    name: str = None
    preferred_username: str = None
    inbox: str = None
    outbox: str = None
    followers: str = None
    following: str = None
    public_key: str = None
    public_key_name: str = None
    event_source: str = None
    proxy_url: str = None

    def build(self, visibility=Visibility.PUBLIC):
        """Creates the json-ld representation of the actor."""
        result = {
            "@context": self._build_context(),
            "id": self.id,
            "type": self.type,
            **self._build_public_key(),
            **self._build_endpoints(visibility=visibility),
        }

        if self.preferred_username:
            result["preferredUsername"] = self.preferred_username

        if visibility == Visibility.WEB:
            return result

        if self.name:
            result["name"] = self.name
        elif self.preferred_username:
            result["name"] = self.preferred_username

        return result

    def _build_context(self):
        if self.public_key:
            return [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1",
            ]

        return "https://www.w3.org/ns/activitystreams"

    def _build_public_key(self):
        if self.public_key:
            return {
                "publicKey": {
                    "id": f"{self.id}#{self.public_key_name}",
                    "owner": self.id,
                    "publicKeyPem": self.public_key,
                }
            }
        return {}

    def _build_endpoints(self, visibility):
        result = {}

        if visibility == Visibility.WEB:
            return result

        if self.inbox:
            result["inbox"] = self.inbox
        else:
            result["inbox"] = self.id

        if self.outbox:
            result["outbox"] = self.outbox
        else:
            result["outbox"] = self.id

        if visibility != Visibility.OWNER:
            return result

        endpoints = self._build_user_endpoints()
        if endpoints:
            result["endpoints"] = endpoints

        if self.followers:
            result["followers"] = self.followers
        if self.following:
            result["following"] = self.following

        return result

    def _build_user_endpoints(self):
        endpoints = {}
        if self.event_source:
            endpoints["eventSource"] = self.event_source
        if self.proxy_url:
            endpoints["proxyUrl"] = self.proxy_url
        return endpoints
