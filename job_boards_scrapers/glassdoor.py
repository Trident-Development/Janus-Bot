from job_boards_scrapers.base import JobBoard, JobBoardType

# TODO: Implement a Glassdoor job scraper


class Glassdoor(JobBoard):
    def __init__(self) -> None:
        self._job_board_name = JobBoardType.GLASSDOOR
