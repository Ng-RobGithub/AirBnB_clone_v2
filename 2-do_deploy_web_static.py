#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import run, put, env
from os.path import exists

# Define the list of web server IP addresses
env.hosts = ['ubuntu@54.167.152.167', 'ubuntu@54.159.2.24']
# Define the user to connect to the remote hosts
env.user = 'ubuntu'
# Specify the path to your private key file if you're using key-based authentication
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        web_static = '/data/web_static/releases/' + archive_name.split('.')[0]

        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Create the release directory
        run('mkdir -p {}'.format(web_static))

        # Uncompress the archive to the releases directory
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, web_static))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_name))

        # Move contents to proper location
        run('mv {}/web_static/* {}'.format(web_static, web_static))

        # Remove the now empty web_static directory
        run('rm -rf {}/web_static'.format(web_static))

        # Update the symbolic link
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(web_static))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
