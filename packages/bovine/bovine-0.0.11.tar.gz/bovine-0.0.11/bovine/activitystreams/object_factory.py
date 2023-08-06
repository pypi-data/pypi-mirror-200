from dataclasses import dataclass, field
from typing import Set


@dataclass
class Object:
    """A dataclass representing an `ActivityStreams Object
    <https://www.w3.org/TR/activitystreams-vocabulary/#object-types>`_"""

    type: str
    attributed_to: str = None
    followers: str = None
    id: str = None
    published: str = None
    to: Set[str] = field(default_factory=set)
    cc: Set[str] = field(default_factory=set)

    name: str = None
    summary: str = None
    content: str = None
    source: dict = None

    in_reply_to: str = None
    url: str = None
    tag: Set[dict] = None

    def as_public(self):
        self.to.add("https://www.w3.org/ns/activitystreams#Public")
        if self.followers:
            self.cc.add(self.followers)
        return self

    def as_unlisted(self):
        if self.followers:
            self.to.add(self.followers)
        self.cc.add("https://www.w3.org/ns/activitystreams#Public")
        return self

    def build(self):
        result = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": self.type,
            "attributedTo": self.attributed_to,
            "to": list(self.to),
            "cc": list(self.cc - self.to),
        }

        extra_fields = {
            "id": self.id,
            "inReplyTo": self.in_reply_to,
            "published": self.published,
            "source": self.source,
            "name": self.name,
            "url": self.url,
            "summary": self.summary,
            "content": self.content,
            "tag": self.tag,
        }

        for key, value in extra_fields.items():
            if value:
                result[key] = value

        return result


class ObjectFactory:
    """ObjectFactory usually created through a BovineClient"""

    def __init__(self, actor_information):
        self.information = actor_information

    def note(self):
        """Creates a Note Object"""
        return Object(
            attributed_to=self.information["id"],
            type="Note",
            followers=self.information.get("followers"),
        )

    def article(self):
        """Creates an Article Object"""
        return Object(
            attributed_to=self.information["id"],
            type="Article",
            followers=self.information.get("followers"),
        )
