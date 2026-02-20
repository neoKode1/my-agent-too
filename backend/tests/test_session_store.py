"""Tests for the in-memory SessionStore."""

from app.models.conversation import Message, Role, SessionStatus, WizardSession
from app.services.session_store import SessionStore


def _fresh_store() -> SessionStore:
    return SessionStore()


# ---------- create ----------

def test_create_returns_session():
    store = _fresh_store()
    session = store.create()
    assert isinstance(session, WizardSession)
    assert session.status == SessionStatus.GATHERING


def test_create_stores_session():
    store = _fresh_store()
    session = store.create()
    assert store.get(session.session_id) is session


# ---------- get ----------

def test_get_missing_returns_none():
    store = _fresh_store()
    assert store.get("nonexistent") is None


# ---------- save ----------

def test_save_updates_timestamp():
    store = _fresh_store()
    session = store.create()
    original_ts = session.updated_at
    session.messages.append(Message(role=Role.USER, content="test"))
    store.save(session)
    assert session.updated_at >= original_ts


def test_save_persists_changes():
    store = _fresh_store()
    session = store.create()
    session.status = SessionStatus.RECOMMENDING
    store.save(session)
    fetched = store.get(session.session_id)
    assert fetched is not None
    assert fetched.status == SessionStatus.RECOMMENDING


# ---------- list ----------

def test_list_empty():
    store = _fresh_store()
    assert store.list_sessions() == []


def test_list_multiple():
    store = _fresh_store()
    store.create()
    store.create()
    assert len(store.list_sessions()) == 2


# ---------- delete ----------

def test_delete_existing():
    store = _fresh_store()
    session = store.create()
    assert store.delete(session.session_id) is True
    assert store.get(session.session_id) is None


def test_delete_nonexistent():
    store = _fresh_store()
    assert store.delete("nope") is False

