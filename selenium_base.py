from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions as Exceptions
from selenium.webdriver.common.proxy import *
from selenium.common.exceptions import *


import random
import time
import urllib
import logging
import re


class SeleniumBase(object):
    def __init__(self, driver = None, headless:bool=False):
        self.driver = driver or self.get_driver(self.get_profile(), headless=headless)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver:
            self.driver.close()

    def element_screenshot(self, driver, element, filename):
        bounding_box = (
            element.location['x'], # left
            element.location['y'], # upper
            (element.location['x'] + element.size['width']), # right
            (element.location['y'] + element.size['height']) # bottom
        )
        return self.bounding_box_screenshot(driver, bounding_box, filename)

    def get_profile(self):
        firefox_profile = webdriver.FirefoxProfile()
        #firefox_profile.set_preference('browser.privatebrowsing.autostart', True)
        firefox_profile.set_preference('http.response.timeout', 5)
        firefox_profile.set_preference('dom.max_script_run_time', 5)
        #firefox_profile.set_preference("network.proxy.type", 1)
        #firefox_profile.set_preference("network.proxy.socks", "192.168.76.1")
        #firefox_profile.set_preference("network.proxy.socks_port", 1080)
        #firefox_profile.set_preference("network.proxy.socks_version", 5)
        #firefox_profile.set_preference("intl.accept_languages", "en-US, en")

        #firefox_profile.set_preference("privacy.item.cookies", "True")
        return firefox_profile

    def get_driver(self, profile, headless:bool=False):
        options = Options()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        #driver.minimize_window()
        driver.set_page_load_timeout(20)
        driver.set_window_position(1000, 500)
        driver.set_window_size(1350, 768)

        driver.get("http://www.google.com/404page")

        """
        driver.add_cookie({'name' : 'intl_locale', 'value' : 'en_US', 'domain' : '.domain.com',
                           'Path' : '/', '' : '', '' : ''})
        """
        return driver

    def bounding_box_screenshot(self, driver, bounding_box, filename):
        driver.save_screenshot(filename)
        base_image = Image.open(filename)
        cropped_image = base_image.crop(bounding_box)
        base_image = base_image.resize(cropped_image.size)
        base_image.paste(cropped_image, (0, 0))
        base_image.save(filename)
        return base_image

    def waiter(self, timeout = 30):
        return WebDriverWait(self.driver, timeout)

    def wait_for_element_by_id(self, id, timeout = 30):
        return self.waiter().until(
            EC.presence_of_element_located((By.ID, id))
        )

    def wait_for_element_by_name(self, name, timeout = 30):
        return self.waiter().until(
            EC.presence_of_element_located((By.NAME, name))
        )

    def wait_for_element_by_css_selector(self, selector, value = None, timeout = 30):
        return self.waiter().until(
            EC.presence_of_element_located((By.CSS_SELECTOR,  '[{}]'.format(selector))) if value is None else
            EC.presence_of_element_located((By.CSS_SELECTOR, '[{}="{}"]'.format(selector, value)))
        )

    def wait_for_element_by_formcontrolname(self, name, timeout = 30):
        return self.wait_for_element_by_css_selector('formcontrolname', name)

    def wait_for_element_by_attribute(self, name, timeout = 30):
        return self.wait_for_element_by_css_selector(name)

    def wait_for_element_by_xpath(self, xpath, timeout = 30):
        return self.waiter(timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def find_element_by_xpath(self, xpath_locator):
        try:
            return self.driver.find_element_by_xpath(xpath_locator)
        except NoSuchElementException:
            return None

    def find_elements_by_xpath(self, xpath_locator):
        try:
            return self.driver.find_elements_by_xpath(xpath_locator)
        except NoSuchElementException:
            return None

    def load_whole_page(self, expected_class):
        prior = 0
        while True:
            self.scroll_down()
            current = len(
                self.waiter().until(EC.presence_of_all_elements_located((By.CLASS_NAME, expected_class))))
            self.logger.debug('load_whole_page {0}'.format(current))
            if current == prior:
                return current
            prior = current

    def next_sibling(self, elem):
        return self.driver.execute_script("""
            return arguments[0].nextElementSibling
        """, elem)

    def set_location(self, url):
        self.logger.debug('set_location to "{0}"'.format(url))
        self.driver.execute_script('window.location.href = "{0}";'.format(url))

    def get(self, url):
        self.logger.debug('get "{0}"'.format(url))
        self.driver.get(url)

    def random_sleep(self, t = 7, min_time = 3):
        r = random.randint(min_time, t)
        self.logger.debug('(sleeping {0})'.format(r))
        time.sleep(r)

    def sleep(self, t = 1):
        self.logger.debug('(sleeping {0})'.format(t))
        time.sleep(t)

