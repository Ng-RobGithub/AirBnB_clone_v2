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

    time = datetime.now()
    archive_name = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    create = local('tar -czvf versions/{} web_static'.format(archive_name))
    if create.succeeded:
        return 'versions/' + archive_name
    else:
        return None
