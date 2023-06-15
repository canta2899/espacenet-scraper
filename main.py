from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from random import randint
import time
import re
import sys
from bs4 import BeautifulSoup
from parser import parse_input_file, sys, write_output_header
from utils import dispose_webdriver, get_webdriver

OUTPUT_FILE = "output.csv"

def get_html_text(html_content) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def number_of_entries(driver):
    time.sleep(3)
    res_found = driver.find_element(by=By.XPATH, value="/html/body/div/div/div[2]/div/div[3]/div[1]/div[1]/h1/span[2]/div/div/div")
    text = get_html_text(res_found.get_attribute("innerHTML"))
    return int(text.split(" ")[0])

def ensure_description_tab(driver):
    category_btn = driver.find_element(by = By.CSS_SELECTOR, value="button[data-qa='tabsSelect_resultDescription']")

    current_category = category_btn.get_attribute("aria-label")

    if current_category.lower().strip() == "description":
        return

    category_btn.click()
    time.sleep(2)
    modal_entry = driver.find_element(by = By.XPATH, value="/html/body/div[2]/div[3]/ul/li[2]")
    modal_entry.click()
    time.sleep(4)

def rank_patent(driver: webdriver.Chrome, input_entry) -> None:

    link = input_entry["link"]
    driver.get(link)
    loaded, items = scroll_until_full_load(driver)
    print(f"Fully loaded {loaded} items")
    time.sleep(5)

    for item in items:
        try:

            item.click()
            time.sleep(5)
            pub_element = driver.find_element(by = By.CSS_SELECTOR, value="a[data-qa='publicationNumber']")
            publication_number = get_html_text(pub_element.get_attribute("innerHTML"))
        except:
            continue

        try:
            ensure_description_tab(driver)
            details = driver.find_element(by = By.CSS_SELECTOR, value=".details div[dir='ltr']")
            description = get_html_text(details.get_attribute("innerHTML"))
            ranking(description, input_entry, publication_number)
            time.sleep(6)
        except KeyboardInterrupt:
            pass
        except:
            with open(input_entry["filename"], "a") as f:
                f.write(f"{publication_number};skipped due to error (missing description data)\n")
        finally:
            driver.implicitly_wait(5)

def scroll_until_full_load(driver):

    time.sleep(3)
    num_entries = number_of_entries(driver)
    time.sleep(3)

    scrollable_element = driver.find_element(by=By.XPATH, value="/html/body/div/div/div[2]/div/div[3]/div[1]/div[1]/div[5]")

    loaded = 0
    items = [] 

    while loaded < num_entries:
        items = scrollable_element.find_elements(by=By.TAG_NAME, value="article")
        loaded = len(items)
        driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", scrollable_element)
        time.sleep(randint(3, 6))

    return loaded, items

def ranking(description, input_entry, code):
    output_file = input_entry["filename"]
    line = f"{code};"

    for term in input_entry["words"]:
        current_word = term["word"]
        weight = term["weight"]
        pattern = re.compile(current_word)
        matches = pattern.findall(description)
        count = len(matches)
        computed_rank = count * weight
        line += f"{computed_rank};"

    print(line)

    with open(output_file, "a") as f:
        f.write(f"{line}\n")



def main():
    input_file_path = sys.argv[1]

    entries = parse_input_file(input_file_path)

    driver: webdriver.Chrome = get_webdriver()

    try:
        for entry in entries:
            write_output_header(entry)
            rank_patent(driver, entry)
    except KeyboardInterrupt:
        print("Closing...")
    finally:
        dispose_webdriver(driver)

if __name__ == '__main__':
    main()

