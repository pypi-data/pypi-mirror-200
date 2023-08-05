import socket
import re
import logging
import subprocess
import sys
from smawe_tools import OS_NAME, List
from types import ModuleType
from typing import Union

try:
    from retrying import retry
except ModuleNotFoundError as e:
    logging.warning(e)
    logging.warning("\033[1;34mInstalling dependent libraries: retrying\033[0m")
    completed_process = subprocess.run("{} -m pip install retrying".format(sys.executable))
    if completed_process.returncode:
        logging.info("Using a temporary solution.\n\033[1;34mPlease manually install the retrying library if "
                     "necessary\033[0m")
        from smawe_tools import retry
    else:
        from retrying import retry


def _get_domain(url: str) -> str:
    try:
        _m = re.search(r"//(.*?)/", url.strip())
        return _m.group(1)
    except AttributeError:
        _m = re.search(r"//(.*)", url.strip())
        if _m:
            return _m.group(1)

    raise ValueError("please enter a valid url")


def get_ip(url: str = None, domain: str = None) -> List[str]:
    """
    get url or domain ip
    :param url: can be url or domain
    :param domain: website domain
    :return: list[str]
    """
    if url:
        url = url.strip()
        if "/" not in url:
            _domain = url
        else:
            _domain = _get_domain(url)
        try:
            (hostname, alias_list, ipaddr_list) = socket.gethostbyname_ex(_domain)
            return ipaddr_list
        except socket.gaierror as e:
            logging.error("please enter valid url")
            logging.error(e)

    if domain:
        domain = domain.strip()
        try:
            (hostname, alias_list, ipaddr_list) = socket.gethostbyname_ex(domain)
            return ipaddr_list
        except socket.gaierror as e:
            logging.error("please enter valid domain")
            logging.error(e)

    raise ValueError("please enter valid parameters")


@retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
def _install_requires(cmd: Union[str, List[str]]):
    subprocess.run(cmd)


def _run_cmd(cmd: Union[str, List[str]]) -> ModuleType:
    completed_p = subprocess.run(cmd)
    if not completed_p.returncode:
        logging.info("\033[1;34mThe dependent library is already installed\033[0m")
    else:
        _install_requires(cmd)
    try:
        import requests
    except ModuleNotFoundError as e:
        logging.error("Dependency library installation failed. Please check your network")
        logging.error("Failure Reason: {}".format(e))
        raise ValueError("The dependent library was not successfully installed: requests") from e
    else:
        return requests


def get_pubnet_ip() -> str:
    try:
        import requests
    except ModuleNotFoundError:
        logging.warning("\033[1;34mInstalling dependent libraries: requests\033[0m")
        if OS_NAME == "Windows":
            requests = _run_cmd("{} -m pip install requests".format(sys.executable))
        else:
            requests = _run_cmd("{} -m pip install requests".format(sys.executable).split())
    r = requests.get("https://www.httpbin.org/get")
    return r.json()['origin']


__all__ = ['get_ip', 'get_pubnet_ip']
