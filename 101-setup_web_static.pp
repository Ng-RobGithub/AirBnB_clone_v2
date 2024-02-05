# Ensure Nginx is installed
package { 'nginx':
ensure => installed,
}

# Ensure Nginx is running
service { 'nginx':
ensure => running,
enable => true,
}

# Create necessary directories
file { '/data':
ensure => directory,
owner  => 'ubuntu',
group  => 'ubuntu',
}

file { '/data/web_static':
ensure => directory,
owner  => 'root',
group  => 'root',
}

file { '/data/web_static/releases':
ensure => directory,
owner  => 'root',
group  => 'root',
}

file { '/data/web_static/shared':
ensure => directory,
owner  => 'root',
group  => 'root',
}

file { '/data/web_static/releases/test':
ensure => directory,
owner  => 'root',
group  => 'root',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
ensure  => file,
content => "<html>\n<head>\n</head>\n<body>\n  Holberton School\n</body>\n</html>",
owner   => 'root',
group   => 'root',
}

# Create symbolic link
file { '/data/web_static/current':
ensure  => link,
target  => '/data/web_static/releases/test',
owner   => 'root',
group   => 'root',
}
