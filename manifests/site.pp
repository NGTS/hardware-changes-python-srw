class { "apt": 
  always_apt_update => true,
}

class { "::mysql::server":
  require => Class["apt"],
}

class { "::mysql::client":
  require => Class["apt"],
}

class { "::mysql::bindings":
  python_enable => true,
  require => Class["apt"],
}

class { "python":
  version => "system",
  pip => true,
  virtualenv => true,
}

package { "pip":
  provider => "pip",
  ensure => "latest",
  require => Class["python"],
}

python::requirements { "/vagrant/requirements.txt": 
  require => Class["::mysql::client"],
}
