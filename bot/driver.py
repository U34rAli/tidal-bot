import os
from abc import ABC, abstractclassmethod
from selenium import webdriver

class Driver(ABC):
    base_path = ""

    def __init__(self, base_path) -> None:
        self.base_path = base_path

    @abstractclassmethod
    def get_driver(self):
        pass


class Chrome(Driver):

    def __init__(self, base_path) -> None:
        super().__init__(base_path)

    def get_driver(self):
        return webdriver.Chrome(executable_path= os.path.join(self.base_path, "chromedriver.exe")) 

class Firefox(Driver):

    def __init__(self, base_path) -> None:
        super().__init__(base_path)

    def get_driver(self):
        return webdriver.Firefox(executable_path= os.path.join(self.base_path, "geckodriver.exe"))


def get_driver(base_path, browser = "chrome"):
    if browser.lower() == "firefox":
        return Firefox(base_path).get_driver()
    else:
        return Chrome(base_path).get_driver()
