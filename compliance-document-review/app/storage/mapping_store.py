from threading import Lock
from typing import Dict, Optional


class MappingStore:
    """
    Development storage for per-document PII mappings.

    Production replacement:
    - PostgreSQL / encrypted database
    - Redis with encryption
    - managed secrets/data store

    Raw mappings must never be included in outbound AI payloads.
    """

    def __init__(self):
        self._store: Dict[str, Dict[str, str]] = {}
        self._lock = Lock()

    def save(
        self,
        document_id: str,
        mapping: Dict[str, str],
    ) -> None:

        with self._lock:
            self._store[document_id] = mapping.copy()

    def get(
        self,
        document_id: str,
    ) -> Optional[Dict[str, str]]:

        with self._lock:
            mapping = self._store.get(document_id)

            if mapping is None:
                return None

            return mapping.copy()

    def delete(
        self,
        document_id: str,
    ) -> None:

        with self._lock:
            self._store.pop(document_id, None)


mapping_store = MappingStore()