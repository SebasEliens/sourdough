"""Pytest fixtures. Clear in-memory store before each test for isolation."""

import pytest

from app.main import _messages


@pytest.fixture(autouse=True)
def clear_messages():
    _messages.clear()
    yield
    _messages.clear()
