from typing import Dict
from abc import ABC, abstractmethod

from selenium_base import SeleniumBase
import logging

class TaxerDriverBase(ABC):
    def __init__(self):
        self._base_url = 'https://taxer.ua'
        self._token = None
        self._cookies = dict()

    def get_url(self, path):
        return '{}/{}'.format(self._base_url, path)

    @property
    def token(self) -> str: return self._token

    @token.setter
    def token(self, value): self._token = value

    @property
    def cookies(self) -> Dict[str, str]: return self._cookies

    @cookies.setter
    def cookies(self, value): self._cookies = value


    @property
    def base_url(self) -> str: return self._base_url

class TaxerDriver(SeleniumBase, TaxerDriverBase):
    def __init__(self, username, password, driver=None, headless:bool=False):
        SeleniumBase.__init__(self, driver=driver, headless=headless)
        TaxerDriverBase.__init__(self)
        self.logger = logging.getLogger(__class__.__name__)
        self.username = username
        self.password = password
        self.cookies = None
        self.login_url = self.get_url('ru/login')

    def goto_main(self):
        self.set_location(self.base_url)
        self.random_sleep(2, 1)

    def check_logged_in(self):
        try:
            e = self.driver.find_element_by_xpath('//a[contains(@class, "tt-accountant-account-name")]')
            return not e.is_displayed()
        except:
            pass
        return False

    def login(self, username=None, password=None):
        self.username = username or self.username
        self.password = password or self.password
        self.logger.info('Logging in {0} via url {1}'.format(self.username, self.login_url))
        self.driver.get(self.login_url)
        self.wait_for_element_by_formcontrolname('email').send_keys(self.username)
        self.wait_for_element_by_attribute('ppassword').send_keys(self.password)
        self.wait_for_element_by_xpath('//button[@type="submit"]').click()
        self.wait_for_element_by_css_selector('routerlink', '/my/settings/account')
        self.cookies = dict((c['name'], c['value']) for c in self.driver.get_cookies())
        self.token = self.cookies['XSRF-TOKEN']
        self.logger.debug('Current location {0}'.format(self.driver.current_url))

    def initialize(self):
        self.goto_main()
        r = self.check_logged_in()
        if not r:
            self.login()
            r = self.check_logged_in()
        return r

    def quit(self):
        self.driver.quit()

from http.cookies import SimpleCookie

class TaxerTokenDriver(TaxerDriverBase):
    def __init__(self, cookies:str):
        super().__init__()
        self.logger = logging.getLogger(__class__.__name__)
        if cookies is not None and isinstance(cookies, str):
            cookie = SimpleCookie()
            cookie.load(cookies)
            self.cookies = {key:morsel.value for (key,morsel) in cookie.items()}
            self.token = self.cookies['XSRF-TOKEN']
            self.logger.debug(f'Using token {self.token}')