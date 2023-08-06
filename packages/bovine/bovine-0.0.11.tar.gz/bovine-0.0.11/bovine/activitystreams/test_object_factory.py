from .object_factory import ObjectFactory


def test_object_factory():
    object_factory = ObjectFactory({"id": "actor_id", "followers": "followers"})

    note = object_factory.note().as_public()
    note.content = "text"
    result = note.build()

    assert set(result.keys()) == {
        "@context",
        "attributedTo",
        "content",
        "type",
        "to",
        "cc",
    }

    assert result["to"] == ["https://www.w3.org/ns/activitystreams#Public"]
    assert result["cc"] == ["followers"]
