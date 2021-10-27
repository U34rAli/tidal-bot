from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class Tidal:
    browser: webdriver.Chrome
    url: str
    implicit_wait = 2  # seconds
    username: str
    password: str

    def __init__(self, browser, url, username, password) -> None:
        self.browser = browser
        self.url = url
        self.username = username
        self.password = password

    def __wait_tag_by_sec(self, tag, by, sec):
        """
        return True Element if Login is required.
        """
        element = None
        try:
            element = WebDriverWait(self.browser, sec).until(
                EC.presence_of_element_located((by, tag))
            )
        except Exception as e:
            print("Element not found. Name: ", tag)
        finally:
            return element

    def __enter_username(self):
        element = self.__wait_tag_by_sec('email', By.ID, 10)
        element.send_keys(self.username)

    def __enter_password(self):
        element = self.__wait_tag_by_sec('password', By.ID, 10)
        element.send_keys(self.password)

    def __press_login_btn(self):
        element = self.__wait_tag_by_sec('//button/div[text()="Log In"]', By.XPATH, 10)
        element.click()

    def __press_login_continue_btn(self):
        element = self.__wait_tag_by_sec('recap-invisible', By.ID, 10)
        element.click()

    def __perform_login(self, login_btn):
        
        login_btn.click()
        time.sleep(10)
        self.__enter_username()
        time.sleep(5)
        self.__press_login_continue_btn()
        time.sleep(5)
        self.__enter_password()
        time.sleep(5)
        self.__press_login_btn()


    def __login_check(self):
        element = self.__wait_tag_by_sec("login-button", By.ID, 5)
        if element:
            try:
                time.sleep(5)
                self.__perform_login(element)
                return True
            except Exception as e:
                print("Unable to login. Error! ", e)
                return False
        return True

    def __get(self):
        self.browser.get(self.url)

    def play_song(self):
        self.__get()
        time.sleep(5)
        self.__login_check()
