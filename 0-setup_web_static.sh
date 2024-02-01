#!/usr/bin/env bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary folders and files
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
echo -e "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo rm -f /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
sudo sed -i "/location \/hbnb_static {/i \\\talias /data/web_static/current/;" "$nginx_config"

# Restart Nginx
sudo service nginx restart

# Exit successfully
exit 0
