from typing import Union

from job_boards_scrapers.base import JobBoard
from job_boards_scrapers.base import JobBoardType
from job_boards_scrapers.base import JobInfo


# TODO: Implement a Glassdoor job scraper


class Glassdoor(JobBoard):
    def __init__(self) -> None:
        self._job_board_name = JobBoardType.GLASSDOOR

    def get_job_info(self, job: Union[str, int]) -> JobInfo:
        return super().get_job_info(job)
