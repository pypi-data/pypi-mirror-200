import argparse
import logging
from datetime import timedelta 
from timeit import default_timer as timer
import json

from rc.cli.command import CmdBase
from rc.cli.utils import run_command_on_subprocess
from rc.cli.utils import *
from rc.utils.request import get_repo_commit_id

logger = logging.getLogger(__name__)

class CmdGet(CmdBase):
    def __init__(self, args):
        super().__init__(args)
    def run(self):
        start = timer()
        # prompt_to_get()
        repo = get_repo()
        version = self.args.version
        commit_id = get_repo_commit_id(json.dumps({"repo_name":repo, "version":version}))
        # if not get_dvc_data_status():
        user_input = input("Are you sure you want to get it? [y/n]").lower()
        if user_input == 'y':
            print("Files downloading...") 
            run_command_on_subprocess('git reset --hard {}'.format(commit_id)) 
            run_command_on_subprocess('dvc pull -f') 
            print("Files downloaded successfully") 
            logger.debug('DOWNLOAD TIME {0}'.format(timedelta(seconds=timer()-start))) 
        else:
            print("Please enter valid input")

        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Get File or folder. Use: `rctl get`"
    REPO_DESCRIPTION = (
        "Get File or folder. Use: `rctl get`"
    )

    repo_parser = subparsers.add_parser(
        "get",
        parents=[parent_parser],
        description=REPO_DESCRIPTION,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    repo_parser.add_argument(
        "-v", 
        "--version", 
        nargs="?", 
        default=None,
        type=int,
        help="Repo commit version",
    )
    repo_parser.set_defaults(func=CmdGet)
