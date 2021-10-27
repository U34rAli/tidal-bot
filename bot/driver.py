import os
from abc import ABC, abstractclassmethod
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox import firefox_profile


class Driver(ABC):
    base_path = None
    driver = None

    def __init__(self, base_path, driver) -> None:
        self.base_path = base_path
        self.driver = driver

    @abstractclassmethod
    def _get_user_agent(self):
        pass


class Chrome(Driver):
    def __init__(self, base_path) -> None:
        self.base_path = base_path
        driver = webdriver.Chrome(
            executable_path=os.path.join(self.base_path, "chromedriver.exe"),
            chrome_options=self._get_user_agent(),
        )

        super().__init__(base_path, driver)


    def _get_user_agent(self):
        opts = Options()
        opts.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
        )

        return opts


class Firefox(Driver):
    def __init__(self, base_path) -> None:
        driver = webdriver.Firefox(
            executable_path=os.path.join(self.base_path, "geckodriver.exe"),
            firefox_profile=self._get_user_agent(),
        )

        super().__init__(base_path, driver)

    def _get_user_agent(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        )

        return profile


def get_driver(base_path, browser="chrome"):
    driver = {"chrome": Chrome, "firefox": Firefox}
    
    return driver[browser](base_path).driver
