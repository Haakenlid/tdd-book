""" Deployment of Django website using pyvenv-3.4 and git """
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/Haakenlid/tdd-book.git'
GIT_DJANGO_PACKAGE = 'https://github.com/django/django/archive/stable/1.7.x.zip'
PYVENV = 'pyvenv-3.4'


def deploy():
    # Folders are named something like www.example.com
    # or www.staging.example.com for production or staging
    venv_name = site_name = env.host
    site_folder = '/srv/%s' % (site_name,)
    source_folder = '%s/source' % (site_folder,)
    venv_folder = '%s/venv/%s' % (site_folder, venv_name,)
    global_venv_folder = '/home/%s/.venvs/' % (env.user)

    print(
        'global_venv_folder: %s \n site_folder: %s \n source_folder: %s \n venv_folder: %s' %
        (global_venv_folder, site_folder, source_folder, venv_folder)
    )
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, site_name)
    _update_virtualenv(source_folder, venv_folder, global_venv_folder)
    _update_static_files(source_folder, venv_folder)
    _update_database(source_folder, venv_folder)


def _create_directory_structure_if_necessary(site_folder):
    """ Ensure basic file structure in project. """
    for subfolder in ('database', 'static', 'venv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    """ Updates files on staging server with current git commit on dev branch. """
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    """ Populates django settings with some security settings differs between dev, staging and production server. """
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,),
        )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        key = ''.join(random.SystemRandom().choice(chars) for n in range(50))
        append(secret_key_file, "SECRET_KEY= '% s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder, venv_folder, global_venv_folder):
    """ Create or update python virtual environment with the required python packages. """
    if not exists(venv_folder + '/bin/pip'):
        run('%s %s' % (PYVENV, venv_folder,))
        run('%s/bin/pip install %s' % (venv_folder, GIT_DJANGO_PACKAGE, ))
        run('ln -s %s %s' % (venv_folder, global_venv_folder))

    run('%s/bin/pip install -r %s/requirements.txt' % (
        venv_folder, source_folder,
    ))


def _update_static_files(source_folder, venv_folder):
    """ Move images, js and css to staticfolder to be served directly by nginx. """
    run('%s/bin/python %s/manage.py collectstatic --noinput' % (venv_folder, source_folder))


def _update_database(source_folder, venv_folder):
    """ Run database migrations if required by changed apps. """
    run('cd %s && %s/bin/python manage.py migrate --noinput' % (
        source_folder, venv_folder,
    ))
