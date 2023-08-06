from datetime import date, datetime, timezone
from typing import Any, Union, Optional
from contextlib import suppress

from dateutil import parser


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def utcnow_ms() -> datetime:
    dt = utcnow()

    return dt.replace(microsecond=int(dt.microsecond / 1_000) * 1_000)


def utcnow_sec() -> datetime:
    return utcnow().replace(microsecond=0)


def parsedt(value: str) -> datetime:
    dt_value = parser.parse(value)

    if dt_value.tzinfo is None:
        return dt_value.replace(tzinfo=timezone.utc)

    return dt_value.astimezone(timezone.utc)


def parsedt_ms(dt: str) -> datetime:
    _dt = parsedt(dt)

    return _dt.replace(microsecond=int(_dt.microsecond / 1_000) * 1_000)


def parsedt_sec(dt: str) -> datetime:
    return parsedt(dt).replace(microsecond=0)


def try_parsedt(dt: Any) -> Optional[datetime]:
    with suppress(ValueError, TypeError, parser.ParserError):
        return parsedt(dt)

    return None


def isoformat(dt: Union[date, datetime]) -> str:
    assert isinstance(dt, (date, datetime))

    if isinstance(dt, datetime):
        if dt.tzinfo is not None:  # second if, because datetime is date...
            dt = dt.astimezone(timezone.utc)
    else:
        dt = datetime(year=dt.year, month=dt.month, day=dt.day)

    dt = dt.replace(tzinfo=timezone.utc)

    return dt.isoformat().replace('+00:00', 'Z')


def try_isoformat(dt: Any) -> Optional[str]:
    if not dt:
        return None

    if isinstance(dt, (date, datetime)):
        return isoformat(dt)
    elif isinstance(dt, str):
        return dt
    elif isinstance(dt, bytes):
        return str(dt, 'utf8')

    return None
