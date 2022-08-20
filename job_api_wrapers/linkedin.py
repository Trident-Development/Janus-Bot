from http.client import InvalidURL
from typing import Optional, Union

import requests

from .datatypes import JobInfo


def get_job_info(url_or_id: Union[str, int]) -> Optional[dict]:
    response = requests.get(
        f"https://geek-pursuit.herokuapp.com/linkedin/job-info",
        params={"job_url_or_id": url_or_id},
    )
    if response.status_code == 400:
        raise InvalidURL()

    payload = response.json()

    if response.status_code == 500 or not payload["success"]:
        return None

    return JobInfo.from_payload(payload["data"][0])
