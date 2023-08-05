import logging
import os
from pathlib import Path
from pydoc import stripid
import subprocess
import sys
from rc.utils import DEBUG
from multiprocessing import cpu_count

logger = logging.getLogger(__name__)

class RctlValidSubprocessError(Exception):
    def __init__(self, msg, *args):
        assert msg
        self.msg = msg
        logger.error(msg)
        super().__init__(msg, *args)

def fix_subparsers(subparsers):
    subparsers.required = True
    subparsers.dest = "cmd"

def get_git_url(cwd):
    result = subprocess.run('git config --get remote.origin.url', capture_output=True, shell=True, cwd=cwd)    
    stdout = str(result.stdout, 'UTF-8')
    return stripid(stdout)

def get_repo():
    result = subprocess.run('git config --get remote.origin.url', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').split("/")[-1].replace('.git', '')
    return stdout.strip()

def trim_str_n_t(str):
    return ' '.join(str.split())

def get_dvc_data_status():
    result = subprocess.run('dvc status', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').strip()
    # stdout_line = stdout.splitlines()
    # stdout_line = list(map(trim_str_n_t, stdout_line))
    if stdout.find('modified') != -1:
        return True  
    return False

def current_commit_hash():
    result = subprocess.run('git rev-parse HEAD', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8')
    return stdout.strip()

def is_current_version_stable():
    from rc.utils.request import get_commit_version, get_repo_version
    repo = get_repo()
    commit_id = current_commit_hash()
    repo_version = get_repo_version(repo)
    commit_version = get_commit_version(commit_id)
    if not commit_version:
        logger.debug("Repo version not found.")
        return True

    if commit_version == repo_version:
        return True
    else:
        logger.debug("Local repo version is not stable")
        print("ERROR: You can not upload from older version. Please use `rc get` to get latest version.")
        sys.exit(50)

def get_min_cpu():
    process = 2
    cpu = cpu_count()
    if cpu>4:
        process = int(cpu/4)
    return process        

def get_dir_file(path):
    dvc_file = Path(f'{path}.dvc')
    if not dvc_file.is_file():
        logger.debug("DVC file not found.")
        print("Something went wrong")
        sys.exit(50)
    dvc_read = open(dvc_file, "r")
    md5_dir = ''
    for line in dvc_read.readlines():
        if line.find('- md5') != -1:
            md5_dir = line.split(":")[-1].strip()
    if not md5_dir:
        logger.error(".dir file not found.")
        sys.exit(50)
    return md5_dir

def get_only_valid_dir(dir):
    if not dir.startswith("."):
        return True
    else:
        return False

def trim_slash(str):
    if str.endswith("/"):
        str = str.rsplit("/", 1)[0] 
    return str

def get_all_data_folder():
    directory = os.getcwd()
    dirs = next(os.walk(directory))[1]
    filtered = list(filter(get_only_valid_dir, dirs))
    return filtered

def compare_dot_dvc_file(dir_path):
    dvc_file = Path(f'{dir_path}.dvc')
    if dvc_file.is_file():
        return True
    
def back_slash_trim(dirs):
    filtered = list(map(trim_slash, dirs))
    return filtered

def run_command_on_subprocess(command, cwd=None, err_skip=False):
    logger.debug(command)
    if cwd:
        result = subprocess.run(command, capture_output=True, shell=True, cwd=cwd)
        stderr = str(result.stderr, 'UTF-8')
        stdout = str(result.stdout, 'UTF-8')
        if DEBUG:
            if stdout:                        
                logger.debug("STD OUT {}".format(stdout)) 
                return True

            if stderr:            
                if not err_skip:
                    raise RctlValidSubprocessError(stderr)
                else:
                    logger.debug("STD ERR {}".format(stderr))
                
    else:
        result = subprocess.run(command, capture_output=True, shell=True)
        stderr = str(result.stderr, 'UTF-8')
        stdout = str(result.stdout, 'UTF-8')
        if DEBUG:
            if stdout:                        
                logger.debug("STD OUT {}".format(stdout)) 
                return True

            if stderr:            
                if not err_skip:
                    raise RctlValidSubprocessError(stderr)
                else:
                    logger.debug("STD ERR {}".format(stderr))
                

def repo_name_valid(name):
    for c in name:        
        if c == '_':
            raise RctlValidSubprocessError("Error: Bucket name contains invalid characters")
    if len(name) <3 or len(name)>63:
        raise RctlValidSubprocessError("Error: Bucket names should be between 3 and 63 characters long")   