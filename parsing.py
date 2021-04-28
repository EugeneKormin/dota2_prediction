from browser import Browser
from selenium import webdriver
from variables import executable_path


class Parsing(object):
    def __init__(self, match_id):
        browser = Browser()
        html_code = browser.get_html_from_match_id()
        print(html_code)
