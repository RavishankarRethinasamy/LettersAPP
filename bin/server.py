import os
import logging
import sys

possible_topdir = os.path.normpath(os.path.join(
    os.path.abspath(os.path.join(sys.argv[0], os.pardir, os.pardir))))

if os.path.exists(os.path.join(possible_topdir, 'app', '__init__.py')):
    sys.path.insert(0, possible_topdir)

from app import letters_app
from common import config


def run():
    try:
        port, host = (config.args.get("MAIN.port"), config.args.get("MAIN.host"))
        logging.info(f'Starting Letters App On {host}:{port}')
        letters_app.app.run(host, port, threaded=True)
    except Exception as e:
        sys.stderr.write(f"ERROR :: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    run()
