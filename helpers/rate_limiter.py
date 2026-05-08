import time
from collections import deque

_buckets: dict[int, deque] = {}

WINDOW_SECONDS = 60
MAX_MESSAGES = 20


def is_rate_limited(user_id: int) -> bool:
    """Returns True if the user has exceeded the message rate limit."""
    now = time.monotonic()
    bucket = _buckets.setdefault(user_id, deque())

    # Drop timestamps outside the window
    while bucket and now - bucket[0] > WINDOW_SECONDS:
        bucket.popleft()

    if len(bucket) >= MAX_MESSAGES:
        return True

    bucket.append(now)
    return False
