from typing import Optional

import requests

from linkedin_profile_api_wrappers.datatypes import LinkedinProfile


def get_profile(url_or_public_id: str) -> Optional[LinkedinProfile]:
    response = requests.get(
        f"https://geek-pursuit.herokuapp.com/linkedin-user-profile",
        params={"url_or_public_id": url_or_public_id},
    )
    payload = response.json()
    if response.status_code != 200 or not payload["success"]:
        return None

    return LinkedinProfile.from_payload(payload["data"])
