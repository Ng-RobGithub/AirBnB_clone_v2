#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the web_static folder"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Creates a .tgz archive from the contents of the web_static folder"""
    try:
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

        # Check if the command was successful (exit code 0)
        if result.return_code == 0:
            print("Archive created successfully:", archive_name)
            return archive_name
        else:
            raise Exception("Failed to create archive. Command returned non-zero exit code.")
        except Exception as e:
            print("Error:", str(e))
            return None


        if __name__ == "__main__":
            # Execute do_pack function when script is run directly
            do_pack()
