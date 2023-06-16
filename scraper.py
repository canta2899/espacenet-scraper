from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from csv_helper import CsvHelper
from utils import get_html_text
from selenium import webdriver
from random import randint
from ranker import Ranker
from typing import Tuple
from input import Input
import paths
import time


class Scraper:
    
    input : Input 
    driver : webdriver.Chrome
    time_increase : int


    def __init__(self, headless : bool = False, time_increase : int = 1) -> None:
        self.driver = self.__get_webdriver(headless)
        self.time_increase = time_increase


    def __get_webdriver(self, headless: bool) -> webdriver.Chrome:
        opt: Options = Options()
        opt.headless = headless
        return webdriver.Chrome(options=opt)


    def quit(self) -> None:
        self.driver.quit()


    def start(self, input : Input) -> None:
        self.input = input
        self.driver.get(self.input.link)
        self.sleep(5)


    def __get_num_entries(self) -> int:
        self.sleep(3)

        res_found : WebElement = self.driver.find_element(
            by=By.XPATH,
            value=paths.NUM_ENTRIES)

        text = get_html_text(res_found.get_attribute("innerHTML") or "")

        return int(text.split(" ")[0])


    def sleep(self, seconds : int) -> None :
        time.sleep(seconds * self.time_increase)
    

    def sleep_random(self, min : int, max : int) -> None:
        time.sleep(randint(min * self.time_increase, max * self.time_increase))


    def scroll_until_full_load(self) -> Tuple[int, list[WebElement]]:
        self.sleep(3)
        num_entries : int = self.__get_num_entries()
        self.sleep(3)

        scrollable_element : WebElement = self.driver.find_element(
            by=By.XPATH,
            value=paths.SCROLL_SECTION)

        loaded : int = 0
        items : list[WebElement] = [] 

        while loaded < num_entries:

            items = scrollable_element.find_elements(
                by=By.TAG_NAME,
                value="article")

            loaded = len(items)

            self.driver.execute_script(
                "arguments[0].scroll(0, arguments[0].scrollHeight);",
                scrollable_element)

            self.sleep_random(3, 6)

        return loaded, items


    def wait_description_tab(self) -> None:
        max_attemps = 5
        sleep_interval = 6
        num_attemps = 0

        while num_attemps <= max_attemps:
            try:
                self.ensure_description_tab()
                break
            except Exception:
                num_attemps += 1
                self.sleep(sleep_interval)



    def ensure_description_tab(self) -> None:
        category_btn : WebElement = self.driver.find_element(
            by = By.CSS_SELECTOR,
            value=paths.CATEGORY_BTN_CSS)

        current_category : str = category_btn.get_attribute("aria-label") or ""

        if current_category.lower().strip() == "description": return

        category_btn.click()
        self.sleep(2)

        modal_entry : WebElement = self.driver.find_element(
            by = By.XPATH,
            value=paths.DESCRIPTION_MODAL_ENTRY)

        modal_entry.click()
        self.sleep(4)


    def rank_patents(self, ranker : Ranker, output : CsvHelper) -> None:
        num_items, items = self.scroll_until_full_load()

        print(f"Fully loaded {num_items} elements")
        self.sleep(5)

        for item in items:

            try:
                item.click()
                self.sleep(5)

                pub_element = self.driver.find_element(
                    by = By.CSS_SELECTOR,
                    value=paths.PUB_ELEMENT_CSS)

                publication_number : str = get_html_text(pub_element.get_attribute("innerHTML") or "")

                self.wait_description_tab()

                details = self.driver.find_element(
                    by = By.CSS_SELECTOR,
                    value=paths.DETAILS_TAB_CSS)

                description : str = get_html_text(details.get_attribute("innerHTML") or "")
                rank_output = ranker.rank(publication_number, description, self.input)
                self.sleep(6)
                output.write_line(rank_output)
            except Exception as e:
                print(e)
                continue

