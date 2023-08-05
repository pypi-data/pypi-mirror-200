import json
import logging
import os
import subprocess
from rc.cli.utils import get_repo
from rc.utils.request import RctlValidRequestError, get_config_value_by_key, update_repo_lock
from rc.utils import DEBUG

logger = logging.getLogger(__name__)
level = logging.INFO
if DEBUG:
    level = logging.DEBUG
logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S') 


class RctlParserError(Exception):
    """Base class for CLI parser errors."""
    def __init__(self):
        logger.error("Parser error")
        super().__init__("Parser error")

class RctlValidReqError(Exception):
    def __init__(self, msg, *args):
        assert msg
        self.msg = msg
        logger.error(msg)
        super().__init__(msg, *args)

def parse_args(argv=None):
    from .parser import get_main_parser
    parser = get_main_parser()
    args = parser.parse_args(argv)
    args.parser = parser
    return args

def valid_requirement():
    # try:        
    #     subprocess.run(['mc', '--version'], capture_output=True)
    # except OSError as err:        
    #     raise RctlValidReqError('minio cli not found! Please install minio cli')
    try:        
        subprocess.run(['gh', '--version'], capture_output=True)
    except OSError as err:        
        raise RctlValidReqError('ERROR: git hub cli not found! Please install git hub cli from https://cli.github.com')
    try:        
        subprocess.run(['git', '--version'], capture_output=True)
    except OSError as err:        
        raise RctlValidReqError('git not found! Please install git')
        
    # if not os.environ.get("GH_TOKEN"):
    #     raise RctlValidReqError("Error: GH_TOKEN not found. Please add GH_TOKEN Environment Variable")
    
    # if not os.environ.get("MINIO_ENDPOINT"):
    #     raise RctlValidReqError("Error: MINIO_ENDPOINT not found. Please add GH_TOKEN Environment Variable")

    # if not os.environ.get("MINIO_SECRET_ACCESS_KEY"):
    #     raise RctlValidReqError("Error: MINIO_SECRET_ACCESS_KEY not found. Please add MINIO_SECRET_ACCESS_KEY Environment Variable")

    # if not os.environ.get("MINIO_ACCESS_KEY_ID"):
    #     raise RctlValidReqError("Error: MINIO_ACCESS_KEY_ID not found. Please add MINIO_ACCESS_KEY_ID Environment Variable")

def main(argv=None):
    repo = get_repo()
    try:
        os.environ['GH_TOKEN'] = get_config_value_by_key('gh_token')
        valid_requirement()
        args = parse_args(argv)
        cmd = args.func(args)
        cmd.do_run()
    except KeyboardInterrupt as exc:
        logger.exception(exc)
        # update_repo_lock(repo, json.dumps({"locked":False}))
    except RctlParserError as exc:
        # logger.error(exc)
        ret = 254
        # update_repo_lock(repo, json.dumps({"locked":False}))
    except RctlValidReqError as exc:
        print(exc.msg)
        # update_repo_lock(repo, json.dumps({"locked":False}))
    except RctlValidRequestError as exc:
        ret = 254
        # update_repo_lock(repo, json.dumps({"locked":False}))
    except Exception as exc:  # noqa, pylint: disable=broad-except
       logger.exception(exc)
    #    update_repo_lock(repo, json.dumps({"locked":False}))
    
