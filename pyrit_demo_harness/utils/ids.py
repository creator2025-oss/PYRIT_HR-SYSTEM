from __future__ import annotations

import time
import uuid


def new_execution_id() -> str:
    """Return a new UUID4 as string for run identifiers."""

    return str(uuid.uuid4())


def current_timestamp() -> float:
    """Return current UNIX timestamp as float seconds."""

    return time.time()
