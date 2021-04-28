from selenium import webdriver
from variables import executable_path
from read_config import url
from time import sleep


class Browser(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=executable_path)

    def maximize_window(self):
        self.driver.maximize_window()

    def open_web_page(self):
        self.driver.get(url=url)

    def find_element(self, how, object_):
        if how == "id":
            found_object = self.driver.find_element_by_id(object_)
        elif how == "xpath":
            found_object = self.driver.find_element_by_xpath(xpath=object_)
        elif how == "name":
            found_object = self.driver.find_element_by_name(name=object_)
        return found_object

    def get_html_code(self):
        html_code = self.driver.page_source
        return html_code

    def close_browser(self):
        self.driver.close()

    def get_html_from_match_id(self, browser, match_id):
        browser.open_web_page()
        browser.maximize_window()
        sleep(5)
        search_box = browser.find_element(how="xpath", object_="/html/body/div[1]/div[2]/div/div/a").click()
        sleep(3)
        input_box = browser.find_element(how="id", object_="q")
        input_box.send_keys(str(match_id))
        search_button = browser.find_element(how="name", object_="commit").click()
        html_code = browser.get_html_code()
        #browser.close_browser()
        return html_code


