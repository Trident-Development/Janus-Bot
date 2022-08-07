from levels_salary_scraper.base import Salary, SalaryInfo

class Levels(Salary):

    _MAIN_VIEW_PREFIX = "https://www.levels.fyi/companies/"
    _MAIN_VIEW_SUFFIX = "/salaries/software-engineer"

    def __init__(self) -> None:
        self._level_key = ""
        self._total_key = ""
        self._base_key = ""
        self._stock_key = ""
        self._bonus_key = ""


    def get_salary_info(self, company):
        return self._extract_from_comapny_view(self._MAIN_VIEW_PREFIX + company + self._MAIN_VIEW_SUFFIX)