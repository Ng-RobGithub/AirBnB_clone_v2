#!/usr/bin/env bash

# Update package lists and install Nginx
sudo apt-get update
sudo apt-get -y install nginx

# Allow Nginx HTTP traffic
sudo ufw allow 'Nginx HTTP'

# Create necessary folders and files
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html

# Populate index.html with content
sudo echo -e "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo rm -f /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve /hbnb_static
nginx_config="/etc/nginx/sites-available/default"
sudo sed -i '/listen 80 default_server/a \ \ location \/hbnb_static {\n\talias /data/web_static/current/;\n}' "$nginx_config"

# Restart Nginx
sudo service nginx restart
