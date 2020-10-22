__author__ = "Peter Detzner"
__maintainer__ = "Peter Detzner"
__version__ = "0.0.1a"
__status__ = "Developement"

import urllib
import http.client
import logging

MAX_CHECK = 100

logger = logging.getLogger(__name__)

# check if the server is running, otherwise wait until


def webserver_is_running(_server_address, _port):
    do_forever = True
    max_check_counter = 0
    while do_forever:
        logger.info("CheckServerRunning, retry %s/%s",
                    str(max_check_counter), str(MAX_CHECK))
        max_check_counter += 1
        if max_check_counter == MAX_CHECK:
            logger.info("CheckServerRunning maximum retries reached")
            do_forever = False
        try:
            temp_url = f"http://{_server_address}:{_port}"
            logger.info("CheckServerRunning Try to access: %s", temp_url)
            urllib.request.urlopen(temp_url)
            logger.info("CheckServerRunning is available %s", temp_url)
            do_forever = False
        except urllib.error.HTTPError as err:
            logger.error("CheckServerRunning HTTPError: %s", str(err.code))
        except urllib.error.URLError as err:
            logger.error("CheckServerRunning URLError")
        except http.client.HTTPException as err:
            logger.error("CheckServerRunning HTTPException: %s", str(err))
        finally:
            logger.error("CheckServerRunning Failed")
    logger.info("CheckServerRunning_done")
