logrotated
==========

[![Build Status](https://travis-ci.org/nir0s/logrotated.svg?branch=master)](https://travis-ci.org/nir0s/logrotated)
[![PyPI](http://img.shields.io/pypi/dm/logrotated.svg)](http://img.shields.io/pypi/dm/logrotated.svg)
[![PypI](http://img.shields.io/pypi/v/logrotated.svg)](http://img.shields.io/pypi/v/logrotated.svg)

Why does your volume keep exploding? It's not ISIS! It's your logs!

`logrotated` is a CLI and Pythonic API for `logrotate` and `LogRotateWin` (SOON!). It aims to make logrotation easier without  having to know the ins and outs of `logrotate`.

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

```shell
$ sudo rotatethis --help
Usage: rotatethis [OPTIONS] PATH...

  Generates a logrotate configuration and deploys it if necessary.

Options:
  -n, --name TEXT                 The name of the logrotation script.
                                  [required]
  -d, --deploy                    Deploy the configuration on the current
                                  machine.
  -f, --frequency [daily|weekly|monthly|yearly]
                                  How often to rotate the files.
  -s, --size TEXT                 Size of file at which rotation will take
                                  place. (e.g. 100k, 100M, 100G)
  -k, --keep TEXT                 How many files to keep when rotating.
  -c, --compress                  Whether to compress rotated log files or
                                  not.
  --create TEXT...                Created new log files using `mod user
                                  password`.
  -l, --delay-compression TEXT    Delay the compression by one file. This will
                                  leave one rotated log file uncompressed
                                  until the next rotation.
  --nocompress                    Negates --compress (in case it is configured
                                  in the main logrotate config.
  --dont-rotate-empty             Do not rotate empty files.
  -m, --ignore-missing            If there are no logs, don't fail.. just
                                  continue.
  --shared-postscript             Run postrotate script only after all logs in
                                  path have been checked.
  -p, --post-rotate TEXT          A script to run post rotation. This is
                                  required by some applications.
  --overwrite                     Whether to overwrite a logrotate config or
                                  not.
  -v, --verbose
  --help                          Show this message and exit.
...
```


## Rotating Paths
```shell
$ rotatethis '/var/log/mongodb/*.log' '/var/log/mongos' --name mongo -v -p '/usr/bin/killall -SIGUSR1 mongod' -p '/usr/bin/killall -SIGUSR1 mongos' --keep 5 --frequency daily --create 644 user group --dont-rotate-empty --deploy
...

INFO - Generating logrotate config...
INFO - Deploying /tmp/logrotate-test/test to /etc/logrotate.d/test...
INFO - Deployment successful!
...

$ cat /etc/logrotate.d/mongo

/var/log/mongodb/*.log /var/log/mongos { 
    daily
    rotate 5
    notifempty
    compress
    create 644 user group 
    postrotate
        /usr/bin/killall -SIGUSR1 mongod
        /usr/bin/killall -SIGUSR1 mongos
    endscript
}
```

### Generating only

If the `--deploy` flag isn't provided, the file will be saved under /tmp/logrotate-NAME/NAME for future use.

## Python API

```python
raise NotImplementedError()
```

## Testing

```shell
git clone git@github.com:nir0s/logrotated.git
cd logrotated
pip install tox
tox
```

## Contributions..

Pull requests are always welcome.
