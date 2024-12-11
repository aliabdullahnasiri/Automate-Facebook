import os
import pickle
import random
import time
from typing import List, Self

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Chrome:
    path: str = ChromeDriverManager().install()

    windows: List[Self] = []

    def __new__(cls, *args, **kwargs) -> Self:
        cls.windows.append(
            instance := super().__new__(cls),
        )

        return instance

    def __init__(self: Self, **kwargs) -> None:

        self.options: Options = Options()

        if kwargs.get("headless", False):
            self.options.add_argument("--headless")

        if kwargs.get("disable_gpu", False):
            self.options.add_argument("--disable-gpu")

        if kwargs.get("disable_infobars", False):
            self.options.add_argument("--disable-infobars")

        if kwargs.get("disable_extensions", False):
            self.options.add_argument("--disable-extensions")

        if kwargs.get("start_maximized", False):
            self.options.add_argument("start-maximized")

        if kwargs.get("no_sandbox", False):
            self.options.add_argument("--no-sandbox")

        if kwargs.get("incognito", False):
            self.options.add_argument("--incognito")

        if kwargs.get("tor", False):
            self.options.add_argument("--proxy-server=socks4://127.0.0.1:9050")

        if kwargs.get("block_notifications", False):
            self.options.add_experimental_option(
                "prefs",
                {
                    "profile.default_content_setting_values.notifications": 1,
                },
            )

        self.service: Service = Service(Chrome.path)

        self.driver: webdriver.Chrome = webdriver.Chrome(
            service=self.service,
            options=self.options,
        )

        if cookies_file := kwargs.get("cookies_file", None):
            if site_url := kwargs.get("site_url", None):
                self.driver.get(site_url)
                time.sleep(5 + random.random())

                if os.path.exists(cookies_file):
                    cookies = pickle.load(open(cookies_file, "rb"))

                    for cookie in cookies:
                        self.driver.add_cookie(cookie)
