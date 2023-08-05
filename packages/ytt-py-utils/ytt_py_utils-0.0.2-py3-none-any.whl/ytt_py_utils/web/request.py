"""
Request Utils
"""
import requests


def download_file(url, path):
    """

    :param url:
    :param path:
    :return:
    """
    myfile = requests.get(url)
    open(path, 'wb').write(myfile.content)