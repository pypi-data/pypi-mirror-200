import base64
import json
import logging
import os
import subprocess
import sys
from functools import lru_cache
from locale import getdefaultlocale
from os.path import dirname, abspath, join
from tempfile import gettempdir

import requests

from gopac.exceptions import (
    CliNotFound, ErrorDecodeOutput, GoPacException, DownloadCancel,
    DownloadPacFileException, SavePacFileException
)

__all__ = ['find_proxy', 'download_pac_file', 'terminate_download_pac_file']

EXTENSION_DIR = join(dirname(abspath(__file__)), 'extension')
ENCODING = (
    'cp866' if sys.platform in ('win32', 'cygwin') else
    (getdefaultlocale()[1] if getdefaultlocale()[1] else 'UTF-8')
)
SERVICE_INFO = {
    'pac_path': '',
    'terminate_download': False
}

logger = logging.getLogger()


def find_shared_library():
    shared_library = list(filter(
        lambda i: not i.endswith('.py') and i != '__pycache__', os.listdir(EXTENSION_DIR)
    ))
    if len(shared_library) != 1:
        raise CliNotFound("CLI not found")
    return join(EXTENSION_DIR, shared_library[0]).replace(r' ', r'\ ')


def get_pac_path(url):
    return join(gettempdir(), base64.b64encode(url.encode()).decode()) + '.pac'


def download_pac_file(url: str) -> str:
    """
    Downloads pac file to temporary directory
    :param url: url to pac file
    :return: path to downloaded file
    """
    def download_hook(*args, **kwargs):
        if SERVICE_INFO['terminate_download']:
            raise DownloadCancel()

    SERVICE_INFO['terminate_download'] = False

    try:
        response = requests.get(
            url, stream=True, timeout=15, hooks={'response': download_hook}
        )
    except DownloadCancel:
        logger.debug('File PAC download cancelled')
        raise
    except Exception as e:
        raise DownloadPacFileException(
            'Error when downloading a file PAC', e
        )

    try:
        SERVICE_INFO['pac_path'] = get_pac_path(url)
        with open(SERVICE_INFO['pac_path'], mode='wb') as pac:
            pac.write(response.content)
        return SERVICE_INFO['pac_path']
    except Exception as e:
        message = 'Error in saving the downloaded pac file'
        logger.exception(message)
        raise SavePacFileException(message, e)


def terminate_download_pac_file():
    SERVICE_INFO['terminate_download'] = True


@lru_cache(maxsize=None)
def find_proxy(pac_file: str, url: str, encoding=None) -> dict:
    """
    Finds a proxy for a URL
    :param pac_file: path to downloaded file
    :param url: target url
    :param encoding: system console encoding
    :return: dict like this {'http': 'url:port', 'https': 'url:port'} or
    an empty dict if no proxy is needed
    """
    cmd = r'{} -pacFile "{}" -url {}'.format(find_shared_library(), pac_file, url)
    encoding = encoding if encoding else ENCODING
    try:
        res = subprocess.check_output(cmd, shell=True).decode(encoding)
    except subprocess.CalledProcessError:
        raise ValueError(
            'The data is not correct, it is not possible to perform a console '
            'command'
        )
    except UnicodeError:
        raise ErrorDecodeOutput(
            'It was not possible to determine the encoding of the system '
            'console and decode the result of the external program'
        )
    except Exception as e:
        raise GoPacException('Unexpected error', e)

    if res.startswith("marshal error"):
        raise GoPacException(
            'The external library was unable to form a response'
        )
    else:
        res = json.loads(res)

        if res['Error']:
            raise GoPacException(res['Error'])

        return res['Proxy']
