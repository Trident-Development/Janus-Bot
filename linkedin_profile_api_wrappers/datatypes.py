from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Experience:
    title: str
    company_name: str
    start_date: str
    end_date: str = None
    duration: str = None
    location: str = None
    company_url: str = None
    description: str = None


@dataclass
class Education:
    school: str
    school_url: str = None
    degree: str = None
    major: str = None
    grade: str = None


@dataclass
class LinkedinProfile:
    name: str
    linkedin_url: str
    profile_image_url: str
    headline: str = None
    about: str = None
    experience: list[Experience] = None
    education: list[Education] = None

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> LinkedinProfile:
        experience_list = [Experience(**exdata) for exdata in payload.pop("experience")]
        education_list = [Education(**eddata) for eddata in payload.pop("education")]
        return cls(experience=experience_list, education=education_list, **payload)
