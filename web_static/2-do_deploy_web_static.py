#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
Usage: fab -f 2-do_deploy_web_static.py do_deploy:<path_to_archive>
"""

from fabric.api import put, run, env
from os.path import exists

# Define the list of hosts
env.hosts = ['54.167.152.167', '54.159.2.24']


def do_deploy(archive_path):
    """
    Distributes the specified archive to the web servers
    Args:
    archive_path (str): Path to the archive to be deployed
    Returns:
    True if deployment is successful, False otherwise
    """

    if not exists(archive_path):
        return False

    try:

        # Extract archive file name and directory name
        file_name = archive_path.split("/")[-1]
        directory_name = file_name.split(".")[0]

        # Define the path on the server
        server_path = "/data/web_static/releases/"

        # Upload the archive to the server's /tmp/ directory
        put(archive_path, '/tmp/')

        # Create the release directory
        run('mkdir -p {}{}/'.format(server_path, directory_name))

        # Extract the archive to the release directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, server_path, directory_name))

        # Delete the uploaded archive from /tmp/
        run('rm /tmp/{}'.format(file_name))

        # Move the contents of the extracted directory to the release directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(server_path, directory_name))

        # Remove the empty web_static directory
        run('rm -rf {}{}/web_static'.format(server_path, directory_name))

        # Update the symbolic link to the new release
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(server_path, directory_name))

        return True
    except Exception as e:
        print("Error:", e)
        return False
