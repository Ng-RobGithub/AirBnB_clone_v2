#!/usr/bin/python3
"""
Fabric script to delete out-of-date archives
Usage: fab -f 100-clean_web_static.py do_clean:number=2 -i ssh-key -u ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import *

# Define the list of hosts
env.hosts = ['54.167.152.167', '54.159.2.24']


def do_clean(number=0):
    """
    Deletes out-of-date archives based on the specified number.
    Args:
    number (int): The number of archives to keep.
    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    # Delete local out-of-date archives
    local_archives = sorted(os.listdir("versions"))
    [local("rm ./versions/{}".format(a)) for a in local_archives[:-number]]

    # Delete remote out-of-date archives
    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [a for a in remote_archives if "web_static_" in a]
        [run("rm -rf ./{}".format(a)) for a in remote_archives[:-number]]
