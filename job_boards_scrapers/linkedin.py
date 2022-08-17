import re
from http.client import InvalidURL
from typing import Optional, Union

from job_boards_scrapers.base import JobBoard, JobBoardType, JobInfo
from utils.validator import is_valid_url


class LinkedIn(JobBoard):
    """
    Represents a LinkedIn job board
    """

    _VIEW_LINK_PREFIX = "https://www.linkedin.com/jobs/view"
    _RECOMMENDED_LINK_REGEX = re.compile(r".*\?currentJobId=[0-9]*")

    def __init__(self) -> None:
        self._job_board_name = JobBoardType.LINKEDIN
        self._title_key = "top-card-layout__title"
        self._company_key = "topcard__org-name-link"
        self._company_pic_key = "sub-nav-cta__image"
        self._img_src_key = "data-delayed-url"
        self._time_ago_key = "posted-time-ago__text"
        self._description_key = "description__text"
        self._location_key = "sub-nav-cta__meta-text"

    def get_job_info(self, job: Union[str, int]) -> Optional[JobInfo]:
        is_direct_view = False

        if isinstance(job, int):
            job = self._url_from_job_id(job)
            is_direct_view = True

        if not is_valid_url(job):
            raise InvalidURL()

        is_direct_view = job.startswith(self._VIEW_LINK_PREFIX)

        # If a link is not a direct view link, there is a possible case that it is a
        # job in a list containing multiple jobs. For example, on LinkedIn, if you click on
        # jobs recommended for you, you will see a split view where on the left hand
        # you can browse jobs and on the right hand you can view the current selected job
        # information. In this case, we want to extract the current selected job only.
        #
        if not is_direct_view:
            if self._is_in_recommended_list(job):
                job_id = self._extract_current_job_id(job)
                job = self._url_from_job_id(job_id)
            else:
                raise InvalidURL()

        # If the job is a directly viewed one, we want to grab only the url resource
        # patch and ignore all the query parameters so we can get a clean url.
        #
        else:
            job = job.split("?")[0]

        return self._extract_from_direct_view(job)

    def _is_in_recommended_list(self, url: str) -> bool:
        return self._RECOMMENDED_LINK_REGEX.search(url)

    def _extract_current_job_id(self, url: str) -> str:
        return self._RECOMMENDED_LINK_REGEX.findall(url)[0].split("=")[-1]

    def _url_from_job_id(self, job_id: Union[str, int]) -> str:
        return f"{self._VIEW_LINK_PREFIX}/{job_id}/"
