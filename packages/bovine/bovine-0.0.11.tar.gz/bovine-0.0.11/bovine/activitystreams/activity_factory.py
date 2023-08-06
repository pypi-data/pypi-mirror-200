from dataclasses import dataclass, field
from typing import Set


@dataclass
class Activity:
    """A dataclass representing an `ActivityStreams Activity
    <https://www.w3.org/TR/activitystreams-vocabulary/#activity-types>`_"""

    type: str
    actor: str = None
    followers: str = None
    id: str = None
    published: str = None
    to: Set[str] = field(default_factory=set)
    cc: Set[str] = field(default_factory=set)

    name: str = None
    summary: str = None
    content: str = None

    target: str = None
    object: str = None

    def as_public(self):
        self.to.add("https://www.w3.org/ns/activitystreams#Public")
        self.cc.add(self.followers)
        return self

    def as_unlisted(self):
        self.to.add(self.followers)
        self.cc.add("https://www.w3.org/ns/activitystreams#Public")
        return self

    def build(self):
        result = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": self.type,
            "actor": self.actor,
            "to": list(self.to),
            "cc": list(self.cc - self.to),
        }

        extra_fields = {
            "id": self.id,
            "published": self.published,
            "name": self.name,
            "summary": self.summary,
            "content": self.content,
            "target": self.target,
            "object": self.object,
        }

        for key, value in extra_fields.items():
            if value:
                result[key] = value

        return result


class ActivityFactory:
    """Basic factory for Activity objects.

    Usally created by a BovineClient"""

    def __init__(self, actor_information):
        self.information = actor_information

    def create(self, note):
        result = Activity(
            type="Create",
            actor=note["attributedTo"],
            cc=set(note["cc"]),
            to=set(note["to"]),
            object=note,
        )
        return result

    def like(self, target):
        result = Activity(
            type="Like",
            actor=self.information["id"],
            object=target,
        )
        return result

    def delete(self, target):
        result = Activity(
            type="Delete",
            actor=self.information["id"],
            object=target,
        )
        return result

    def accept(self, obj):
        result = Activity(
            type="Accept",
            actor=self.information["id"],
            object=obj,
        )
        return result

    def follow(self, obj):
        result = Activity(
            type="Follow",
            actor=self.information["id"],
            object=obj,
        )
        return result
