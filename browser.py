import time
from typing import Optional
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import asyncio

# This package is not working at Oct 2023
import undetected_chromedriver as uc

# new package `seleniumbase` that built on the top of `undetected_chromedriver`
# , which fixes the issue of headless mode not working properly.
from seleniumbase import BaseCase


class Config:
    LOGIN_PAGE = "https://accounts.google.com/v3/signin/identifier?dsh=S1996777714%3A1670403953363964&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F%253FthemeRefresh%253D1&ec=65620&hl=en&passive=true&service=youtube&uilel=3&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=ARgdvAstKnduAcXcaOk-0Klty5KYkL8vl_WMjlojELnpJUJXGAyZuytqhtKKPu1zNZQlKgw1TAQ8eg"
    INPUT_TIMEOUT = 10
    BUTTON_TIMEOUT = 10
    ELEMENT_TIMEOUT = 10
    SLEEP_DURATION = 2


class Driver:
    @staticmethod
    def create_driver():
        # Create and configure a Chrome WebDriver instance with options
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--mute-audio")
        options.add_argument("--headless=new")
        # options.add_argument("--headless")  <-- This old line is deprecated in 4.10.0 of seleniumbase
        # Chrome has a new headless mode that allows users to get the full browser functionality (even run extensions)
        return uc.Chrome(chrome_options=options)

    """ 
    # the following code, is based on `BaseCase`, which I am not sure it is really an API or just a test package. 
    
    def create_driver(self, *args, **kwargs):
        #This method overrides get_new_driver() from BaseCase. 
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--mute-audio")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--headless")
        return webdriver.Chrome(options=options)
    """

class BrowserFactory:
    """
    Here, we try to build up a factory pattern to create different browser instances.
    drivers are async, so we need to use asyncio to create them.
    """
    def __init__(self, option=None):
        self.driver = None
        self.option = option

    def initialize_driver(self):
        self.driver = Driver.create_driver()

    def get_browser(self):
        if self.driver is None:
            self.initialize_driver()

        if self.option == "youtube":
            return YoutubeBrowser(self.driver)
        else:
            return BasicBrowser(self.driver)

class BasicBrowser:
    """
    A basic browser interaction class providing common browser functionality.
    """

    # Initialize the webdriver with the path to chromedriver.exe
    def __init__(self, driver: str):
        """
        Initialize a new instance of the BasicBrowser class.
        """
        self.browser = driver
        self.wait = WebDriverWait(self.browser, Config.ELEMENT_TIMEOUT)

    def open_page(self, url: str):
        """
        Open a web page in the browser.

        Args:
            url (str): The URL of the web page to open.
        """
        self.browser.get(url)

    def close_browser(self):
        """
        Close the browser.
        """
        self.browser.close()

    def find_element(self, by: By, value: str):
        """
        Find an element on the web page.

        Args:
            by (By): The method used to locate the element (e.g., By.ID).
            value (str): The value used for locating the element.

        Returns:
            WebElement: The located web element.
        """
        try:
            return self.wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            raise Exception(f"Element {by}: {value} not found on the page")

    def add_input(self, by: By, value: str, text: str):
        field = self.find_element(by, value)
        field.send_keys(text)

    def click_button(self, by: By, value: str):
        button = self.find_element(by, value)
        button.click()

    def press_enter(self, by: By, value: str):
        field = self.find_element(by, value)
        field.send_keys(Keys.ENTER)

    def element_screenshot(self, by: By, value: str, img_name="screenshot.png"):
        ele = self.find_element(by, value)
        ele.screenshot(img_name)

    def _wait_for_url_change(self, initial_url):
        try:
            self.wait.until(EC.url_changes(initial_url))
            return True
        except TimeoutException:
            return False

class YoutubeBrowser:
    """
    A synchronous Browser class designed to interact with the YouTube website.
    """

    def __init__(self, driver: str):
        self.driver = driver
        self.browser = None
        self.wait = None

    def sync_init(self):
        # Initialize the browser and wait in a synchronous manner
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, Config.ELEMENT_TIMEOUT)

    def _try_click_signup_button(self):
        try:
            print("trying to click the signup button")
            time.sleep(2)  # wait for 2 seconds to load the webpage
            self.click_button(
                by=By.XPATH,
                value='//*[@id="buttons"]/ytd-button-renderer/yt-button-shape/a/yt-touch-feedback-shape/div/div[2]',
            )
            return True
        except:
            return False

    def click_button(self, by, value):
        # Implement your click_button method here using the synchronous WebDriver methods
        pass

# You'll need to implement the `click_button` method with the appropriate WebDriver code.


class YoutubeBrowser:
    """
    A synchronous Browser class designed to interact with the YouTube website.
    """

    def __init__(self, driver: str):
        self.driver = driver
        self.browser = None
        self.wait = None

    def init(self):
        # Initialize the browser and wait
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, Config.ELEMENT_TIMEOUT)

    def _try_click_signup_button(self):
        try:
            print("trying to click the signup button")
            time.sleep(2)  # wait for 2 seconds to load the webpage
            self.click_button(
                by=By.XPATH,
                value='//*[@id="buttons"]/ytd-button-renderer/yt-button-shape/a/yt-touch-feedback-shape/div/div[2]',
            )
            return True
        except:
            return False

    def login_youtube(self, username: str, password: str, login_page: str = None):
        """
        Log into YouTube with the provided username and password.

        Args:
            username (str): The YouTube username.
            password (str): The YouTube password.
            login_page (str): Google login page URL. Defaults to None. And it will use the default login page.
        """
        if login_page is None:
            login_page = Config.LOGIN_PAGE

        """Here, selenium goes to the login page, locates the login block, and then fills in the username and password."""
        self.init()
        self.open_page(login_page)
        self.add_input(By.XPATH, '//*[@id="identifierId"]', username)
        self.click_button(By.XPATH, '//*[@id="identifierNext"]/div/button/span')
        self.add_input(By.NAME, "Passwd", password)
        self.click_button(By.XPATH, '//*[@id="passwordNext"]/div/button')

        print("login_youtube() completed.")

    def response_to_live_chat(self, text):
        self.add_input(by=By.ID, value="input", text=text)
        self.press_enter(by=By.ID, value="input", text=text)

    def verify_logged_in(self, username: str, password: str, login_page: str = None):
        """
        Respond to a live chat with the specified text.

        Args:
            text (str): The text to send in the live chat.
        """

        """Step 1: redirect to the login page of YouTube."""
        login_page = login_page if login_page else Config.LOGIN_PAGE
        self.init()
        self.open_page(login_page)

        if self._wait_for_url_change(login_page):
            print("Page redirected to the main page.")
        else:
            print("Error: Page did not redirect as expected.")
            self.close_browser()
            sys.exit(1)  # Exit with a non-zero status code to indicate an error

        """Step 2: on the YouTube main page, find and click the login button."""
        if self._try_click_signup_button():
            print("Clicked the signup button.")
        print("YouTube login verification completed.")

        print("YouTube login successfully.")

    def open_page(self, url):
        self.browser.get(url)

    def add_input(self, by, value, text):
        element = self.wait.until(EC.presence_of_element_located((by, value)))
        element.send_keys(text)

    def click_button(self, by, value):
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()

    def _wait_for_url_change(self, old_url):
        return self.wait.until_not(EC.url_matches(old_url))

    def press_enter(self, by, value, text):
        element = self.wait.until(EC.presence_of_element_located((by, value)))
        element.send_keys(text + '\n')

    def close_browser(self):
        self.browser.quit()


    def test_say_something(self, text):
        locator_value = "div#input.yt-live-chat-text-input-field-renderer"
        WebDriverWait(self.browser, Config.INPUT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, locator_value))
        )
        self.add_input(by=By.CSS_SELECTOR, value=locator_value, text=text)
        field = self.browser.find_element(by=By.CSS_SELECTOR, value=locator_value)
        field.send_keys(Keys.ENTER)
        field.clear()
