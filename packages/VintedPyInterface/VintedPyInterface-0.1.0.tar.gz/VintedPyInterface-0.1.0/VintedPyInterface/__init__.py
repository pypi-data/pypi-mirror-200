"""
    VintedPyInterface
    By Alix Hamidou 2023
"""
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dataclasses import dataclass

import time


"""
    VintedPyInterface
    By Alix Hamidou 2023
"""

__version__ = "0.1.0"
__author__ = 'Alix Hamidou'




@dataclass
class SearchSetting:
    category: str
    size: str
    brand: str

    def dict(self) -> dict[str, str]:
        return {
            "categorie": self.category,
            "taille": self.size,
            "marque": self.brand
        }


@dataclass
class Article:
    imgLink: str
    price: float
    link: str
    title: str

class VintedPyInterface:
    driver: webdriver.Chrome

    def __init__(self) -> None:
        ua = UserAgent()
        user_agent = ua.random

        options = Options()
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--headless")  # Lancer Chrome en mode sans tête

        self.driver = webdriver.Chrome(options=options)
        return

    def Search(self, search: SearchSetting) -> list[Article]:
        url: str = "https://www.vinted.fr/catalog?"
        params = [f"{v}" for v in search.dict().values()]
        url += "search_text=" + "+".join(params) + "&order=newest_first"
        
        self.driver.get(url)
        time.sleep(5)
        articlesHTML: list[webdriver.remote.webelement.WebElement] = self.driver.find_elements(By.CLASS_NAME, "feed-grid__item")
        articles: list[Article] = []
        for articleHTML in articlesHTML:
            try:
                imgLink: str = articleHTML.find_element(By.CLASS_NAME, "web_ui__ItemBox__image-container").find_element(By.TAG_NAME, "img").get_attribute("src")
                price: float = float(articleHTML.find_elements(By.CLASS_NAME, "web_ui__Cell__cell")[1].text.split("\n")[0].replace("€", "").replace(",", ".").strip())
                link: str = articleHTML.find_element(By.CLASS_NAME, "web_ui__ItemBox__overlay").get_attribute("href")
                title: str = articleHTML.find_element(By.CLASS_NAME, "web_ui__ItemBox__overlay").get_attribute("title")

                articles.append(Article(imgLink, price, link, title))
            except:
                pass
        return articles
