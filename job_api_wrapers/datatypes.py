from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from dateutil.relativedelta import relativedelta


class MissingTimeUnitError(Exception):
    pass


@dataclass
class JobInfo:
    url: str
    title: str
    summary: str
    company: str
    company_pic_url: str
    description: str
    location: str
    posted_time: datetime

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> JobInfo:
        """
        Create a JobInfo class from the payload returned by the API
        """
        posted_time_ago: str = payload.pop("posted_time_ago")
        time, unit, *_ = posted_time_ago.split()
        time = float(time)

        if unit.startswith("min"):
            posted_time = datetime.now() - relativedelta(minutes=time)
        elif unit.startswith("h"):
            posted_time = datetime.now() - relativedelta(hours=time)
        elif unit.startswith("d"):
            posted_time = datetime.now() - relativedelta(days=time)
        elif unit.startswith("w"):
            posted_time = datetime.now() - relativedelta(weeks=time)
        elif unit.startswith("mo"):
            posted_time = datetime.now() - relativedelta(months=time)
        elif unit.startswith("y"):
            posted_time = datetime.now() - relativedelta(years=time)
        else:
            raise MissingTimeUnitError("A time unit is not being considered!")

        return cls(posted_time=posted_time, **payload)
