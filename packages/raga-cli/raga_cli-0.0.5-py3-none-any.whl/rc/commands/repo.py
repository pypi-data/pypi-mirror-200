import argparse
import json
import logging
import os
from datetime import timedelta
import sys 
from timeit import default_timer as timer
import os, pwd

from rc.cli.command import CmdBase
from rc.cli.utils import run_command_on_subprocess, repo_name_valid, get_git_url
from rc.utils.request import get_config_value_by_key, create_repository, create_repo_lock
from rc.utils.sshKeyGen import ssh_key_set_up
from rc.cli import RctlValidReqError

logger = logging.getLogger(__name__)
   
 

"""
----------------------------
***Bucket Name Validation***
----------------------------
Bucket names should not contain upper-case letters
Bucket names should not contain underscores (_)
Bucket names should not end with a dash
Bucket names should be between 3 and 63 characters long
Bucket names cannot contain dashes next to periods (e.g., my-.bucket.com and my.-bucket are invalid)
Bucket names cannot contain periods - Due to our S3 client utilizing SSL/HTTPS, Amazon documentation indicates that a bucket name cannot contain a period, otherwise you will not be able to upload files from our S3 browser in the dashboard.
"""

class RepoMain():
    def __init__(self) -> None:
        self.CLOUD_STORAGE_BUCKET = get_config_value_by_key('bucket_name')
        self.CLOUD_STORAGE_DIR = get_config_value_by_key('cloud_storage_dir')
        self.CLOUD_STORAGE_LOCATION = f"s3://{self.CLOUD_STORAGE_BUCKET}/{self.CLOUD_STORAGE_DIR}"
        self.INITIAL_COMMIT = get_config_value_by_key('git_initial_commit')
        self.GIT_BRANCH = get_config_value_by_key('git_initial_branch')
        self.GIT_ORG = get_config_value_by_key('git_org')
        self.TAGS = {"dataset", "model"}
        self.created_by = pwd.getpwuid(os.getuid()).pw_name 

    def run_repo_create_subprocesses(self,repo_name):     
        logger.debug(f"Repository Name: {repo_name}")
        
        run_command_on_subprocess("gh config set git_protocol ssh")  
        run_command_on_subprocess("gh repo create {0}/{1} --private --clone".format(self.GIT_ORG, repo_name))    
        run_command_on_subprocess("dvc init", repo_name)    
        run_command_on_subprocess("dvc remote add -d {0} {1}/{2} -f".format(self.CLOUD_STORAGE_BUCKET, self.CLOUD_STORAGE_LOCATION, repo_name), repo_name)           
        run_command_on_subprocess("dvc remote modify {0} secret_access_key {1}".format(self.CLOUD_STORAGE_BUCKET, get_config_value_by_key('remote_storage_secret_key')), repo_name)         
        run_command_on_subprocess("dvc remote modify {0} access_key_id {1}".format(self.CLOUD_STORAGE_BUCKET, get_config_value_by_key('remote_storage_access_key')), repo_name)        
        run_command_on_subprocess("dvc config core.autostage true", repo_name)           
        run_command_on_subprocess("git commit -m '{0}' -a".format(self.INITIAL_COMMIT), repo_name)    
        run_command_on_subprocess("git branch -M {0}".format(self.GIT_BRANCH), repo_name)    
        run_command_on_subprocess("git push --set-upstream origin {0}".format(self.GIT_BRANCH), repo_name)       

    def create_repo(self, args):
        print("Repo creating...")   
        logger.debug(f"START CREATE REPO COMMAND")
        repository_name = args.name       
        repository_tag = args.tag  
        if repository_tag not in self.TAGS:
            logger.error("'{0}' tag is not available. Please choice from {1}".format(repository_tag, self.TAGS))
            sys.exit(50)                      
        self.run_repo_create_subprocesses(repository_name)
        git_repo = get_git_url(repository_name)
        s3_repo = "{1}/{2}".format(self.CLOUD_STORAGE_BUCKET, self.CLOUD_STORAGE_LOCATION, repository_name)    
        req_body = json.dumps({
            "repo_name":repository_name,
            "tag":repository_tag,
            "created_by":self.created_by,
            "git_repo":git_repo.replace('\n', ''),
            "remote_storage_url":s3_repo,
        })
        logger.debug(req_body)

        create_repository(req_body)
        create_repo_lock(json.dumps({"repo_name":repository_name, "user_name":self.created_by, "locked":False}))

        print("Repository has been created. `cd {}`".format(repository_name))    
        logger.debug(f"END CREATE REPO COMMAND")

    def clone_repo(self, args):
        start = timer()
        repository_name = args.name     
        print('Cloning...')
        run_command_on_subprocess("gh repo clone {0}/{1}".format(self.GIT_ORG, repository_name), None, True)      
        run_command_on_subprocess("dvc pull", repository_name, True) 
        print("Repository cloned successfully")
        end = timer()
        logger.debug('CLONE TIME {0}'.format(timedelta(seconds=end-start)))    


class CmdRepo(CmdBase):
    def __init__(self, args):
        super().__init__(args)        
        if getattr(self.args, "name", None):
            self.args.name = self.args.name.lower()            
            repo_name_valid(self.args.name)
        else:
            raise RctlValidReqError("Error: Please provide a valid name, -n")
class CmdRepoCreate(CmdRepo):
    def run(self):     
        repo = RepoMain()        
        if self.args.create:
            repo.create_repo(self.args)
        if self.args.clone:
            repo.clone_repo(self.args)                                    
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Create a new repository."
    REPO_DESCRIPTION = (
        "Create a new repository."
    )

    repo_parser = subparsers.add_parser(
        "repo",
        parents=[parent_parser],
        description=REPO_DESCRIPTION,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    repo_parser.add_argument(
        "-create",
        "--create",
        action="store_true",
        default=False,
        help="Create new repo",
    )

    repo_parser.add_argument(
        "-clone",
        "--clone",
        action="store_true",
        default=False,
        help="Clone new repo",
    )

    repo_parser.add_argument(
        "-n", 
        "--name", 
        nargs="?", 
        help="Name of the repo",
    )


    repo_parser.add_argument(
        "-tag", 
        "--tag", 
        nargs="?", 
        help="Tag of the repo",
    )
    
    repo_parser.set_defaults(func=CmdRepoCreate)
