import logging
import sys
import requests

from rc.utils import BASE_URL

logger = logging.getLogger(__name__)

class RctlValidRequestError(Exception):
    def __init__(self, msg, *args):
        assert msg
        self.msg = msg
        logger.error(msg)
        super().__init__(msg, *args)

def valid_response(response):
    if not isinstance(response, dict):
        raise RctlValidRequestError("Error: HTTP response is not a dict type.")

    if 'success' not in response.keys():
        raise RctlValidRequestError("Error: HTTP response `success` keyword not found.")

    if response['success']:
        if 'data' not in response.keys():
            raise RctlValidRequestError("Error: HTTP response `data` keyword not found.")

        if not len(response['data']):
            raise RctlValidRequestError("Error: HTTP response record not found.")
        return response
    
    else:
        if 'message' not in response.keys():
            raise RctlValidRequestError("Error: HTTP response `message` keyword not found.")
        raise RctlValidRequestError(response["message"])


def make_request(url, method, data = None):
    headers = {'Content-Type': 'application/json'}
    logger.debug("URL: {}".format(url))
    try:
        response = requests.request(method, url, headers = headers, data = data)
        if not (200 <= response.status_code < 300):
            logger.error('HTTP ERROR: {}'.format(response.content))
            if response.json()['status'] == 404:
                raise RctlValidRequestError('Error: Api endpoint not found.')
        return response.json()
    except requests.exceptions.Timeout as e:
        raise RctlValidRequestError(e)
    except requests.exceptions.TooManyRedirects as e:
        raise RctlValidRequestError(e)
    except requests.exceptions.HTTPError as e:
        raise RctlValidRequestError(e)
    except requests.exceptions.RequestException as e:
        raise RctlValidRequestError(e)

def get_config_value_by_key(key):    
    url = f"{BASE_URL}/configs?key={key}"
    response = valid_response(make_request(url, "GET"))
    key_value = response['data']['conf_value']
    logger.debug("KEY VALUE FROM URL: {0} --- VALUE : {1}".format(url, key_value))
    return key_value


def create_repository(obj):
    url = f"{BASE_URL}/repos"
    response = valid_response(make_request(url, "POST", obj))
    data = response['data']
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data


def create_repo_lock(obj):
    url = f"{BASE_URL}/repolock"
    response = valid_response(make_request(url, "POST", obj))
    data = response['data']
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data


def is_repo_lock(repo):
    url = f"{BASE_URL}/repolock?key={repo}"
    response = valid_response(make_request(url, "GET"))
    value = response['data']['locked']
    logger.debug("REPO LOCK VALUE : {0}".format( value))
    if value:
        msg = "Someone is uploading. Please try after some time."
        print(msg)
        raise RctlValidRequestError(msg)
    return value


def update_repo_lock(repo, lock):
    url = f"{BASE_URL}/repolock/{repo}"
    response = valid_response(make_request(url, "PUT", lock))
    data = response['data']
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data


def insert_repo_commit(obj):
    url = f"{BASE_URL}/repocommit"
    response = valid_response(make_request(url, "POST", obj))
    data = response['data']
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data

def get_repo_commit_id(obj):
    url = f"{BASE_URL}/repocommit/data"
    response = valid_response(make_request(url, "POST", obj))
    data = response['data']["commit_id"]
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data

def get_repo_version(repo):
    url = f"{BASE_URL}/repocommit/repo/{repo}"
    response = valid_response(make_request(url, "GET"))
    data = response['data']["version"]
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data
        
def get_commit_version(commit_id):
    url = f"{BASE_URL}/repocommit/commitId/{commit_id}"
    response = valid_response(make_request(url, "GET"))
    data = response['data']["version"]
    logger.debug("RESPONSE VALUE FROM URL: {0} --- VALUE : {1}".format(url, data))
    return data