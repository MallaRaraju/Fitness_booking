from django.utils.timezone import make_aware
from datetime import datetime, time, date
from pytz import timezone


def local_aware(_time: time, _timezone: str) -> time:
    """Convert a naive time (assumed UTC) to a target timezone's local time.

    Args:
        _time (time): Naive time object (assumed to be in UTC).
        _timezone (str): Target timezone string (e.g., "Asia/Kolkata").
                         Defaults to "UTC".

    Returns:
        time: Localized time in the target timezone.

    Example:
        >>> local_aware(time(15, 0), "Asia/Kolkata")
        datetime.time(20, 30)  # 15:00 UTC → 20:30 IST (+5:30)
    """
    if _timezone !='UTC':
        utc_datetime = datetime.combine(date.today(), _time)
        utc_aware = make_aware(utc_datetime, timezone('UTC'))
        local_aware_time = utc_aware.astimezone(timezone(_timezone))
        return local_aware_time.time()

    return _time