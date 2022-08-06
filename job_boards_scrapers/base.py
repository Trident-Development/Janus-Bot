from dataclasses import dataclass
from datetime import timedelta
from typing import Optional
from typing import Union

import html2text
import requests
from bs4 import BeautifulSoup as bs


@dataclass
class JobInfo:
    title: str = None
    company: str = None
    description: str = None
    location: str = None
    posted_time_ago: timedelta = None
    summary: str = None
    company_pic_url: str = None
    url: str = None


class JobBoardType:
    LINKEDIN = "LinkedIn"
    GLASSDOOR = "Glassdoor"


class NeedSubclassImplementationError(Exception):
    """Method needs implementation from subclass"""

    def __init__(self, msg="Need implementation from subclass") -> None:
        super().__init__(msg)


class JobBoard:
    """
    A base class to represent a job board. Subclass it!
    """

    _html2text: html2text.HTML2Text  # Helps render html to string

    # Should be set by subclasses.
    _job_board_name: str  # The name of the job board
    _company_key: str
    _title_key: str
    _time_ago_key: str
    _description_key: str
    _location_key: str
    _company_pic_key: str
    _img_src_key: str
    _link_to_job_in_list: str

    def __init_subclass__(cls) -> None:
        cls._html2text = html2text.HTML2Text()
        cls._html2text.body_width = 0

    def get_job_info(self, job: Union[str, int]) -> JobInfo:
        """
        Get the information about a job posting from its URL.

        Args:
            url (str): Either the URL to the job post, or the ID of the job.

        Returns:
            JobInfo: The information about the job post.
        """
        raise NeedSubclassImplementationError()

    def _extract_from_direct_view(self, url: str) -> Optional[JobInfo]:
        """
        Extract the job information from a direct job view.

        Args:
            url (str): The URL to the job post on LinkedIn.

        Returns:
            Optional[JobInfo]: The basic information of the job.
        """
        response = requests.get(url)
        html = response.content
        soup = bs(html, "lxml")

        posted_time_ago = soup.find_all(class_=self._time_ago_key)
        if not posted_time_ago:
            return None
        posted_time_ago = posted_time_ago[0].get_text(strip=True)

        summary = soup.find("title").get_text()
        job_title = soup.find_all(class_=self._title_key)[0].get_text(strip=True)
        company = soup.find_all(class_=self._company_key)[0].get_text(strip=True)
        location = soup.find_all(class_=self._location_key)[0].get_text(strip=True)
        pic_url = soup.find_all(class_=self._company_pic_key)[0][self._img_src_key]

        desc = soup.find_all(class_=self._description_key)
        desc = desc[0]
        # remove the buttons components
        for data in desc(["button"]):
            data.decompose()
        # render the html to string
        desc = self._html2text.handle(str(desc))

        return JobInfo(
            title=job_title,
            company=company,
            description=desc,
            company_pic_url=pic_url,
            location=location,
            summary=summary,
            posted_time_ago=posted_time_ago,
            url=url,
        )

    def _extract_from_jobs_list(self, url: str) -> Optional[JobInfo]:
        """
        Extract the job information when the job is viewed in list mode

        Args:
            url (str): The URL to the job post

        Returns:
            Optional[JobInfo]: The basic information of the job
        """
        response = requests.get(url)
        html = response.content
        soup = bs(html, "lxml")
        direct_view_url = soup.find_all(class_=self._link_to_job)[0]
        return self._extract_from_direct_view(direct_view_url)

    @property
    def name(self) -> str:
        """Get the name of the job board."""
        return self._job_board_name
