#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the web_static folder"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Creates a .tgz archive from the contents of the web_static folder"""

    # Get current date and time
    now = datetime.now()

    # Format the date and time as specified
    date_time = now.strftime("%Y%m%d%H%M%S")

    # Create the name of the archive
    archive_name = "versions/web_static_" + date_time + ".tgz"

    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")

    # Create the .tgz archive
    result = local("tar -cvzf {} web_static".format(archive_name))

    # Return the path of the archive if successfully created, otherwise None
    if result.succeeded:
        return archive_name
    else:
        return None


if __name__ == "__main__":
    # Execute do_pack function when script is run directly
    do_pack()
