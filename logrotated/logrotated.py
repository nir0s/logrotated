"""
http://www.linuxcommand.org/man_pages/logrotate8.html
"""

import os
import sys
import json
import shutil
import logging
import pkgutil
import tempfile
from distutils.spawn import find_executable

import click
import jinja2

from . import logger

LOGROTATED_PATH = '/etc/logrotate.d'

lgr = logger.init()


def rotate(paths, name, deploy=False, verbose=False, **params):
    lgr.setLevel(logging.DEBUG if verbose else logging.INFO)

    if deploy and not find_executable('logrotate'):
        lgr.error('logrotate was not found on this system. aborting deploy.')
        sys.exit(1)
    params.update(dict(paths=paths, name=name))
    logrotate_config_path = _generate_tmp_file_path(name)
    _generate_from_template(logrotate_config_path, **params)
    if deploy:
        try:
            _deploy_logrotate_config(
                logrotate_config_path,
                os.path.join(LOGROTATED_PATH, name))
        except IOError as ex:
            if 'Permission denied:' in str(ex):
                lgr.error(
                    'Cannot write configuration file to {0}. Note '
                    'that to deploy, you must run logrotated as sudo.'.format(
                        LOGROTATED_PATH))
            else:
                raise IOError(ex)


def _generate_from_template(destination, **params):
    template = pkgutil.get_data(__name__, os.path.join(
        'resources', 'logrotate'))

    pretty_params = json.dumps(params, indent=4, sort_keys=True)
    lgr.debug('Rendering logrotate with params: {0}...'.format(pretty_params))
    generated = jinja2.Environment().from_string(template).render(**params)
    lgr.debug('Writing generated file to {0}...'.format(destination))
    with open(destination, 'w') as f:
        f.write(generated)


def _generate_tmp_file_path(name):
    tmp_dir = os.path.join(tempfile.gettempdir(), 'logrotate-' + name)
    tmp_file_path = os.path.join(tmp_dir, name)
    if not os.path.isdir(tmp_dir):
        os.makedirs(tmp_dir)
    return tmp_file_path


def _deploy_logrotate_config(source, destination):
    lgr.info('Deploying {0} to {1}...'.format(source, destination))
    shutil.move(source, destination)


@click.command()
@click.argument('path', required=True, nargs=-1)
@click.option('-n', '--name', required=True,
              help='The name of the logrotation script.')
@click.option('-d', '--deploy', is_flag=True, default=False,
              help='Deploy the configuration on the current machine.')
@click.option('-f', '--frequency',
              type=click.Choice(['daily', 'weekly', 'monthly', 'yearly']),
              help='How often to rotate the files.')
@click.option('-s', '--size',
              help='Size of file at which rotation will take place. '
              '(e.g. 100k, 100M, 100G)')
@click.option('-k', '--keep',
              help='How many files to keep when rotating.')
@click.option('-c', '--compress', default=True, is_flag=True,
              help='Whether to compress rotated log files or not.')
@click.option('--create', nargs=3,
              help='Created new log files using `mod user password`.')
@click.option('-l', '--delay-compression',
              help='Delay the compression by one file. This will leave one '
              'rotated log file uncompressed until the next rotation.')
@click.option('--nocompress', default=False, is_flag=True,
              help='Negates --compress (in case it is configured in the main '
              'logrotate config.')
@click.option('--dont-rotate-empty', default=False, is_flag=True,
              help='Do not rotate empty files.')
@click.option('-m', '--ignore-missing', default=True, is_flag=True,
              help="If there are no logs, don't fail.. just continue.")
@click.option('--shared-postscript', default=False, is_flag=True,
              help='Run postrotate script only after all logs in path have '
              'been checked.')
@click.option('-p', '--post-rotate', multiple=True,
              help='A script to run post rotation. This is required by some '
              'applications.')
@click.option('--overwrite', default=False, is_flag=True,
              help='Whether to overwrite a logrotate config or not.')
@click.option('-v', '--verbose', default=False, is_flag=True)
def main(path, name, deploy, verbose, **params):
    """Generates a logrotate configuration and deploys it if necessary.
    """
    logger.configure()
    params['post_rotate'] = list(params['post_rotate'])
    rotate(list(path), name, deploy, verbose, **params)
