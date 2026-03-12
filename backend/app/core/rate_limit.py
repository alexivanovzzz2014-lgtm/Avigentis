from collections import defaultdict, deque
from datetime import datetime, timedelta

from fastapi import HTTPException

from app.core.config import settings

_requests: dict[str, deque[datetime]] = defaultdict(deque)


def check_rate_limit(key: str) -> None:
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=1)
    bucket = _requests[key]
    while bucket and bucket[0] < window_start:
        bucket.popleft()
    if len(bucket) >= settings.scan_rate_limit_per_minute:
        raise HTTPException(status_code=429, detail='Rate limit exceeded. Please retry later.')
    bucket.append(now)
