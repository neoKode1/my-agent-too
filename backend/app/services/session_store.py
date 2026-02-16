"""In-memory session store for wizard conversations.

Swap this out for Redis or a database-backed store in production.
"""

from datetime import datetime
from typing import Dict, List, Optional

from app.models.conversation import WizardSession


class SessionStore:
    """Thread-safe-ish in-memory store keyed by session_id."""

    def __init__(self) -> None:
        self._sessions: Dict[str, WizardSession] = {}

    def create(self) -> WizardSession:
        session = WizardSession()
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> Optional[WizardSession]:
        return self._sessions.get(session_id)

    def save(self, session: WizardSession) -> None:
        session.updated_at = datetime.utcnow()
        self._sessions[session.session_id] = session

    def list_sessions(self) -> List[WizardSession]:
        return list(self._sessions.values())

    def delete(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None


# Module-level singleton
sessions = SessionStore()

