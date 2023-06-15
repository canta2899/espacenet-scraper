from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_webdriver() -> webdriver.Chrome:
    opt: Options = Options()
    # opt.headless = True  # False causes the browser to open
    driver: webdriver.Chrome = webdriver.Chrome(options=opt)
    return driver

def dispose_webdriver(driver: webdriver.Chrome) -> None:
    driver.quit()
