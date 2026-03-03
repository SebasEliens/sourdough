"""Pytest fixtures. Reset in-memory store before each test for isolation."""

import pytest

import app.store as store_module
from app.store import InMemoryStore, get_store


@pytest.fixture(autouse=True)
def clear_messages():
    store_module._store = None
    store = get_store()
    assert isinstance(store, InMemoryStore)
    yield
    store_module._store = None
