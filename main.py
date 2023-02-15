import logging
import os
import time
import temptests
from requests import request



console = logging.StreamHandler()
#console.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(name)-20s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
#temptests.serialize()
#exit(0)
""" MAIN SECTION """
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 7080))
    HOST = os.environ.get('HOST', '127.0.0.1')
    HUB = os.environ.get('GRID_HUB', None)
    TAXER_USER = os.environ.get('TAXER_USER', None)
    TAXER_PWD = os.environ.get('TAXER_PWD', None)
    TAXER_TOKEN = os.environ.get('TAXER_TOKEN', None)
    TAXER_COOKIES = os.environ.get('TAXER_COOKIES', None)
    #HUB='http://localhost:4444/wd/hub'

    from app import create_app
    create_app().run(debug=True, host = HOST, port=PORT, use_reloader=TAXER_TOKEN is not None or TAXER_COOKIES is not None)
# geco driver https://github.com/mozilla/geckodriver/releases