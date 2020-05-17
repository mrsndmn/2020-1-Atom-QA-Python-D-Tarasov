class selenoid::service($port='4444') {

  file { "/tmp/nginx.conf":
    ensure => file,
    content => template("nginx/nginx.conf.erb"),
    notify => Service["nginx"]
  }

  firewalld_port { 'Open port selenoid port in the public zone':
    ensure   => present,
    zone     => 'FedoraServer',
    port     => $port,
    protocol => 'tcp',
  }

}
