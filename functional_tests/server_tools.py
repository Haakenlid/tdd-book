from os import path
import subprocess
THIS_FOLDER = path.dirname(path.abspath(__file__))


def create_session_on_server(host, email):
    """ calls a fabric script via the shell to create a new user and login session. Returns a valid session key """
    session_key = subprocess.check_output(
        [
            'fab',
            'create_session_on_server:email={}'.format(email),
            '--host={}'.format(host),
            '--hide=everything, status',
        ],
        cwd=THIS_FOLDER,
    ).decode().strip()
    return session_key


def reset_database(host):
    subprocess.check_call(
        [
            'fab',
            'reset_database',
            '--host={}'.format(host),
        ],
        cwd=THIS_FOLDER,
    )
