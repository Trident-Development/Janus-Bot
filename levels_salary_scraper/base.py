from dataclasses import dataclass
from re import S
import html2text
import requests
from bs4 import BeautifulSoup as bs

@dataclass
class SalaryInfo:
    level: str
    total: str
    base: str
    stock: str
    bonus: str

class Levels:
    def __init__(self, company) -> None:
        self.base_link = "https://www.levels.fyi/companies/" + company + "/salaries/software-engineer"
        
class Salary:
    _html2text: html2text.HTML2Text

    _level_key: str
    _total_key: str
    _base_key: str
    _stock_key: str
    _bonus_key: str

    def __init_sublass__(cls) -> None:
        cls._html2text = html2text.HTML2Text()
        cls._html2text.body_width = 0

    def get_company_info(self, company):
        pass

    def _extract_from_comapny_view(self, url: str):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        response = requests.get(url, headers=headers)
        print(response)
        print(url)
        html = response.content
        soup = bs(html, "lxml")

       
        level = soup.findAll("a", class_="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover css-3aax9m")[2].get_text()
        total = soup.findAll("h6", class_="MuiTypography-root MuiTypography-subtitle1 css-idrr7q")[0].get_text()
        base = soup.findAll("h6")[14].get_text()
        stock = soup.findAll("h6")[16].get_text()
        bonus = soup.findAll("h6")[19].get_text()

        return SalaryInfo(
            level,
            base,
            stock,
            total,
            bonus
        )