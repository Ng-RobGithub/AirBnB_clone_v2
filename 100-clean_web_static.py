#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import local, run, env
from datetime import datetime
import os

# Define the list of web server IP addresses
env.hosts = 'ubuntu@54.167.152.167', 'ubuntu@54.159.2.24'
# Define the user to connect to the remote hosts
env.user = 'ubuntu'


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        number = int(number)
        if number < 0:
            number = 0

            # Get a list of archives sorted by modification time
            archives = sorted(os.listdir('versions'), reverse=True)
            archives_to_keep = archives[:number]

            # Delete unnecessary archives in the versions folder
            for archive in archives:
                if archive not in archives_to_keep:
                    local("rm versions/{}".format(archive))

                    # Get a list of releases sorted by modification time
                    releases = run("ls -t /data/web_static/releases").split()
                    releases_to_keep = releases[:number]

                    # Delete unnecessary archives in the releases folder on each web server
                    for release in releases:
                        if release not in releases_to_keep:
                            run("rm -rf /data/web_static/releases/{}".format(release))

                            return True
                        except Exception as e:
                            return False


                        if __name__ == "__main__":
                            do_clean()
