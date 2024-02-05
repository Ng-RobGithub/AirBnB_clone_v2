#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
Usage: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

# Define the list of hosts
env.hosts = ['54.167.152.167', '54.159.2.24']


def do_pack():
    """
    Generates a .tgz archive containing the contents of the web_static folder
    Returns:
    Path to the created archive if successful, None otherwise
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
            file_name = "versions/web_static_{}.tgz".format(date)
            local("tar -cvzf {} web_static".format(file_name))
            return file_name
    except Exception as e:
            print("Error:", e)
            return None


def do_deploy(archive_path):
    """
    Distributes the specified archive to the web servers and deploys it
    Args:
    archive_path (str): Path to the archive to be deployed
    Returns:
    True if deployment is successful, False otherwise
    """

    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        directory_name = file_name.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive to the server's /tmp/ directory
        put(archive_path, '/tmp/')

        # Create the release directory
        run('mkdir -p {}{}/'.format(path, directory_name))

        # Extract the archive to the release directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, directory_name))

        # Delete the uploaded archive from /tmp/
        run('rm /tmp/{}'.format(file_name))

        # Move the contents of the extracted directory to the release directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, directory_name))

        # Remove the empty web_static directory
        run('rm -rf {}{}/web_static'.format(path, directory_name))

        # Update the symbolic link to the new release
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, directory_name))

        return True
    except Exception as e:
        print("Error:", e)
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers
    Returns:
    True if deployment is successful, False otherwise
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
