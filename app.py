from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from taxer_driver import TaxerDriverBase, TaxerDriver, TaxerTokenDriver
from taxer_api import TaxerApi
from flask import Flask
import os, time
from requests import request
import logging
import logging.config
from temptests import traverse_q

taxerApi:TaxerApi = None

def init_taxer(hub:str, login:str, pwd:str, cookies:str):
    global taxerApi

    if cookies is not None:
        taxer_driver = TaxerTokenDriver(cookies)
    elif login is not None and pwd is not None:
        driver = None if hub is None else \
            webdriver.Remote(
                command_executor=hub,
                desired_capabilities=DesiredCapabilities.CHROME)
        taxer_driver = TaxerDriver(login, pwd, driver=driver)
        taxer_driver.initialize()
    else:
        raise Exception(f'Wrong parameters')
    taxerApi = TaxerApi(taxer_driver)

def wait_for_grid(hub):
    connected:bool = False
    iterations:int = 10
    logger = logging.getLogger(__name__)
    while not connected and iterations > 0:
        try:
            logger.debug(f'Waiting for hub {hub}')
            response = request('GET', f'{hub}/status')
            logger.debug(f'Waiting for hub {hub} -> {response.status_code}, {response.content}')
            resp = response.json()
            if 'value' in resp and 'ready' in resp['value']:
                connected = resp['value']['ready'] == True
        except ValueError as err:
            logger.error(f'Waiting for hub {hub} ValueError {err}', exc_info=1)
        except:
            logger.error(f'Waiting for hub {hub} error', exc_info=1)
            raise
        if not connected:
            time.sleep(1)
            iterations = iterations - 1
    logger.debug(f'Hub {hub} {"connected" if connected else "not connected"}')

def setup_logger(filename:str):
    import yaml
    if os.path.exists(filename):
        with open(filename, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                print(f'Setup logging from {filename}')
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration.')
                logging.basicConfig(level=logging.INFO)
    else:
        print(f'logging config file {filename} not found.')
        logging.basicConfig(level=logging.INFO)

def create_app(config_filename:str = None) -> Flask:
    setup_logger('logging.yaml')
    logger = logging.getLogger(__name__)
    logger.debug(f'access app http://localhost:<port>/docs')
    #traverse_q()

    HUB = os.environ.get('GRID_HUB', None)
    TAXER_USER = os.environ.get('TAXER_USER', None)
    TAXER_PWD = os.environ.get('TAXER_PWD', None)
    #TAXER_TOKEN = os.environ.get('TAXER_TOKEN', None)
    TAXER_COOKIES = os.environ.get('TAXER_COOKIES', None)
    # Check config
    use_token:bool = TAXER_COOKIES is not None
    use_user:bool = TAXER_USER is not None and TAXER_PWD is not None

    if not use_token and not use_token:
        raise Exception('(TAXER_USER and TAXER_PWD) or (TAXER_TOKEN and TAXER_COOKIES) must be set')
    if use_user and HUB is None:
        logger.info(f'GRID_HUB must be set')
    if use_user:
        logger.info(f'Using taxer with {TAXER_USER}')
    if use_token:
        logger.info(f'Using taxer with cookies {TAXER_COOKIES}')

    if use_user and HUB is not None:
        wait_for_grid(HUB)

    init_taxer(HUB, TAXER_USER, TAXER_PWD, TAXER_COOKIES)
    from apis import create_application
    return create_application(config_filename)