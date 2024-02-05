# Configures a web server for deployment of web_static.

# Nginx configuration file
$nginx_conf = "server {
listen 80 default_server;
listen [::]:80 default_server;
add_header X-Served-By ${hostname};
root   /var/www/html;
index  index.html index.htm;
location /hbnb_static {
alias /data/web_static/current;
index index.html index.htm;
}
location /redirect_me {
return 301 https://th3-gr00t.tk;
}
error_page 404 /404.html;
location /404 {
root /var/www/html;
internal;
}
}"

# Ensure nginx package is present and installed
package { 'nginx':
ensure   => 'present',
provider => 'apt'
} ->

# Ensure directory structure is created for web_static deployment
file { '/data':
ensure  => 'directory'
} ->

file { '/data/web_static':
ensure => 'directory'
} ->

file { '/data/web_static/releases':
ensure => 'directory'
} ->

file { '/data/web_static/releases/test':
ensure => 'directory'
} ->

file { '/data/web_static/shared':
ensure => 'directory'
} ->

# Create a test HTML file for web_static deployment
file { '/data/web_static/releases/test/index.html':
ensure  => 'present',
content => "Holberton School Puppet\n"
} ->

# Create a symbolic link to the test HTML file
file { '/data/web_static/current':
ensure => 'link',
target => '/data/web_static/releases/test'
} ->

# Set ownership of /data/ directory to ubuntu user and group
exec { 'chown -R ubuntu:ubuntu /data/':
path => '/usr/bin/:/usr/local/bin/:/bin/'
}

# Ensure directory structure is created for nginx
file { '/var/www':
ensure => 'directory'
} ->

file { '/var/www/html':
ensure => 'directory'
} ->

# Create default HTML files for nginx
file { '/var/www/html/index.html':
ensure  => 'present',
content => "Holberton School Nginx\n"
} ->

file { '/var/www/html/404.html':
ensure  => 'present',
content => "Ceci n'est pas une page\n"
} ->

# Ensure Nginx default site configuration is set to the provided content
file { '/etc/nginx/sites-available/default':
ensure  => 'present',
content => $nginx_conf
} ->

# Restart nginx service
exec { 'nginx restart':
path => '/etc/init.d/'
}
