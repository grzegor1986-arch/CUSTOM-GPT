from events.github_transformer import transform_github_webhook


def test_transform_push_payload() -> None:
    event = transform_github_webhook(
        "push",
        {
            "ref": "refs/heads/main",
            "before": "abc",
            "after": "def",
            "commits": [{"id": "1"}],
            "repository": {"full_name": "acme/repo"},
            "sender": {"login": "octocat"},
        },
    )

    assert event is not None
    assert event.event_type == "push"
    assert event.repository == "acme/repo"
    assert event.payload["after"] == "def"


def test_transform_unsupported_event() -> None:
    event = transform_github_webhook("fork", {"repository": {"full_name": "acme/repo"}})
    assert event is None
