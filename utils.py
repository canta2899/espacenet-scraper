from typing import Union
from bs4 import BeautifulSoup

WordsMapType = list[dict[str, Union[str, int]]]

def get_html_text(html_content : str) -> str:
    soup : BeautifulSoup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

