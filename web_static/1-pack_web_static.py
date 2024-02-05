#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the contents of the web_static folder
Usage: fab -f 1-pack_web_static.py do_pack
"""

from datetime import datetime
from fabric.api import *


def do_pack():
    """
    Compresses the contents of the web_static folder into a .tgz archive
    Returns:
    Path to the created archive if successful, None otherwise
    """

    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = 'web_static_{}.tgz'.format(current_time)
        local('mkdir -p versions')
        local('tar -cvzf versions/{} web_static'.format(archive_name))
        return 'versions/{}'.format(archive_name)
    except Exception as e:
        print("Error:", e)
        return None
