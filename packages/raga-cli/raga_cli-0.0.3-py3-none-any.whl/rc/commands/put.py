import argparse
import json
import logging
from os import path
from datetime import timedelta
from pathlib import Path
import sys 
from timeit import default_timer as timer
from multiprocessing import Pool, cpu_count

from rc.cli.command import CmdBase
from rc.cli.utils import *
from rc.cli import RctlValidReqError

from rc.utils.request import is_repo_lock, update_repo_lock, insert_repo_commit

logger = logging.getLogger(__name__)

def run_put_subprocess(repo, paths, message):
    start = timer()
    is_repo_lock(repo)
    update_repo_lock(repo, json.dumps({"locked":True}))
    print("Files uploading...")   
    paths = back_slash_trim(paths)

    for path in paths:
        dir_add(path)
    
    dir_upload(paths)

    run_command_on_subprocess("git commit -m '{}' -a".format(message), None, True)
    run_command_on_subprocess("git push", None, True)

    update_repo_lock(repo, json.dumps({"locked":False}))
    logger.debug('TOTAL UPLOAD TIME {0}'.format(timedelta(seconds=timer()-start)))
    

def dir_add(path):
    start = timer()
    if compare_dot_dvc_file(path):
        run_command_on_subprocess("dvc commit {0} -f".format(path))
    else:
        run_command_on_subprocess("dvc add {0}".format(path))
    run_command_on_subprocess("git add {0}.dvc".format(path))
    logger.debug('DVC ADD TIME {0}'.format(timedelta(seconds=timer()-start)))


def dir_upload(paths):
    start = timer()
    run_command_on_subprocess("dvc push {0}".format(' '.join(paths)))
    logger.debug('DVC PUSH TIME {0}'.format(timedelta(seconds=timer()-start))) 
    print("Files uploaded successfully")
    

def put(args):
    message = args.message      
    paths = args.path   
    repo = get_repo()

    # is_current_version_stable()

    run_put_subprocess(repo, paths, message)
    
    for path in paths:
        md5_dir = get_dir_file(path)  
        commit_hash = current_commit_hash()
        request_payload = {
            "folder": path,
            "commit_message" : message,
            "repo" : repo,
            "dir_file":md5_dir,
            "commit_id":commit_hash,
        }   
        insert_repo_commit(json.dumps(request_payload))


class CmdPut(CmdBase):
    def __init__(self, args):
        super().__init__(args)
        self.dirs = None
        if not getattr(self.args, "message", None):                               
            raise RctlValidReqError("Error: Please provide a message, -m")
        if getattr(self.args, "path", None):
            self.dirs = [self.args.path]
        else:
            self.dirs = get_all_data_folder()         

    def run(self):
        self.args.path = self.dirs
        put(self.args) 
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Put File or folder. Use: `rctl put <file or folder path> -m <commit message>`"
    REPO_DESCRIPTION = (
        "Put File or folder. Use: `rctl put <file or folder path> -m <commit message>`"
    )

    repo_parser = subparsers.add_parser(
        "put",
        parents=[parent_parser],
        description=REPO_DESCRIPTION,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    repo_parser.add_argument(
        "-m", 
        "--message", 
        nargs="?", 
        help="Commit message",
    )

    repo_parser.add_argument(
        "path", 
        nargs="?", 
        default=None,
        help="File or Folder path",
    )
    
 
    
    repo_parser.set_defaults(func=CmdPut)
