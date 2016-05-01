logrotated
==========

[![Build Status](https://travis-ci.org/nir0s/logrotated.svg?branch=master)](https://travis-ci.org/nir0s/logrotated)
[![PyPI](http://img.shields.io/pypi/dm/logrotated.svg)](http://img.shields.io/pypi/dm/logrotated.svg)
[![PypI](http://img.shields.io/pypi/v/logrotated.svg)](http://img.shields.io/pypi/v/logrotated.svg)

`logrotated` is a CLI and Pythonic API for `logrotate` and `LogRotateWin`. It allows to easily configure logrotation for files and directories without having to know the ins and outs of `logrotate`.

## Features


## Compatibility

Currently, tested on Python 2.6.x and 2.7.x
Will be adding Python 3.x support soon enough.

## Installation

```shell
sudo pip install logrotated
```

For dev:

```shell
sudo pip install https://github.com/nir0s/logrotated/archive/master.tar.gz
```

## Usage

Before using, please read the caveats section!

```shell
$ sudo serv
Usage: serv [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate  Creates a service.
  remove    Stops and Removes a service
  restart   Restarts a service
  start     Starts a service
  status    WIP! Try at your own expense
  stop      Stops a service

...
```


### Creating a service

```shell
$ sudo serv generate /usr/bin/python2 --name MySimpleHTTPServer --args '-m SimpleHTTPServer' --var KEY1=VALUE1 --var KEY2=VALUE2 --deploy --start
...

INFO - Generating files for systemd...
INFO - Generated /tmp/SimpleHTTPServer.service
INFO - Generated /tmp/SimpleHTTPServer
INFO - Deploying systemd service SimpleHTTPServer...
INFO - Deploying /tmp/SimpleHTTPServer.service to /lib/systemd/system/SimpleHTTPServer.service...
INFO - Deploying /tmp/SimpleHTTPServer to /etc/sysconfig/SimpleHTTPServer...
INFO - Starting systemd service SimpleHTTPServer...
INFO - Service created.


...

$ ss -lntp | grep 8000
LISTEN     0      5            *:8000                     *:*

```

If name is omitted, the name of the service (and therefore, the names of the files) will be deduced from the executable's name.

#### Generating only

If the `--deploy` flag isn't provided, files for the service will be generated and saved under a temp folder for you to use. This is useful when generating service files for use elsewhere.

### Controlling a service

NOTE: Existing services which were not created by Serv can also be controlled.

```shell
$ sudo serv stop MySimpleHTTPServer
INFO - Stopping service: MySimpleHTTPServer...
$ ss -lntp | grep 8000
...
$ sudo serv start MySimpleHTTPServer
INFO - Starting service: MySimpleHTTPServer...
$ ss -lntp | grep 8000
LISTEN     0      5            *:8000                     *:*

$ sudo serv restart MySimpleHTTPServer
INFO - Restarting service: MySimpleHTTPServer...
$ ss -lntp | grep 8000
LISTEN     0      5            *:8000                     *:*
...

```

### Retrieving a service's status

IMPORTANT NOTE: serv status is current very buggy. Except it to break and please submit issues.

NOTE: Existing services which were not created by Serv can also be controlled this way.


```shell
$ sudo serv status MySimpleHTTPServer
...

{
    "init_system": "systemd",
    "init_system_version": "default",
    "services": [
        {
            "active": "active",
            "description": "no",
            "load": "loaded",
            "name": "MySimpleHTTPServer.service",
            "sub": "running"
        }
    ]
}

...
```

or for all services of the same init system

```shell
$ sudo serv status
...
```

### Removing a service

NOTE: Existing services which were not created by Serv can also be controlled this way.

```shell
$ sudo serv remove MySimpleHTTPServer
...

INFO - Removing Service: SimpleHTTPServer...
INFO - Service removed.
...

$ ss -lntp | grep 8000
```

### nssm-specific usage pattern

Windows support is provided via the Non-Sucking Service Manager (nssm).

There are some differences between Windows and Linux support. While the API is practically the same, it still requires the user to be a bit more cautious.

For instance, when providing the `--args` flag, single quotes won't do (e.g. '-m SimpleHTTPServer') but rather doubles must be used and cmd must be loaded as Administrator to be able to install the service as it requires elevated privileges.

It's important to note that deploying a Windows service also deploys nssm itself and will not clean it up if a service is removed as it might be used by other services.

## Python API

```python
raise NotImplementedError()
```

Kidding.. it's there, it's easy and it requires documentation.

## How does it work

Serv, unless explicitly specified by the user, looks up the platform you're running on (Namely, linux distro and release unless running on Windows or OS X) and deduces which init system is running on it by checking a static mapping table or an auto-lookup mechanism.

Once an init-system matching an existing implementation (i.e supported by Serv) is found, Serv renders template files based on a set of parameters; (optionally) deploys them to the relevant directories and (optionally) starts the service.

Since Serv is aware of the init system being used, it also knows which files it needs to deploy and to where and which commands it needs to run.

## Caveats and limitations

* Init system identification is not robust. It relies on some assumptions (and as we all know, assumption is the mother of all fuckups). Some OS distributions have multiple init systems (Ubuntu 14.04 has Upstart, SysV and half (HALF!?) of systemd).
* Stupidly enough, I have yet to standardize the status JSON returned and it is different for each init system.
* If anything fails during service creation, cleanup is not performed. This will be added in future versions.
* Currently, all errors exit with the same error level. This will be changed soon.

### Missing directories

In some situations, directories related to the specific init system do not exist and should be created. For instance, even if systemd (`systemctl`) is available, `/etc/sysconfig` might not exist. IT IS UP TO THE USER to create those directories if they don't exist as Serv should not change the system on that level. The exception to the rule is with `nssm`, which will create the required dir (`c:\nssm`) for it to operate.

The user will be notified of which directory is missing.

Required dirs are:

#### Systemd

* `/lib/systemd/system`
* `/etc/sysconfig`

#### SysV

* `/etc/init.d`
* `/etc/default`

#### Upstart

* `/etc/init`

#### Nssm

The directory (`c:\nssm`) will be created for the user in case it doesn't exist.

## Testing

```shell
git clone git@github.com:nir0s/serv.git
cd ld
pip install tox
tox
```

## Contributions..

Pull requests are always welcome to deal with specific distributions or just for general merriment.

### Adding support for additional init-systems.

* Under serv/init, add a file named <init_system_name>.py (e.g. runit.py).
* Implement a class named <init_system_name> (e.g. Runit). See [systemd](https://github.com/nir0s/serv/blob/master/serv/init/systemd.py) as a reference implementation.
* Pass the `Base` class which contains some basic parameter declarations and provides a method for generating files from templates to your class (e.g. `from serv.init.base import Base`).
* Add the relevant template files to `serv/init/templates`. The file names should be formatted as: `<init_system_name>_<init_system_version>.*` (e.g. runit_default).
* In `serv/init/__init__.py`, import the class you implemented (e.g. `from serv.init.runit import Runit`).
