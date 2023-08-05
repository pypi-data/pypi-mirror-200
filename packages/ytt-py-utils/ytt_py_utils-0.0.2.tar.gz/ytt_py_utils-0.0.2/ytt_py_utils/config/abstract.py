# Template file
"""
Config
"""
from abc import ABC, abstractmethod

class Parser(ABC):
    """ Abstract class """
    def __init__(self,):
        """

        :param fpath:
        """
        self.fpath = None
        self.data = None

    @abstractmethod
    def load(self):
        """

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def save(self):
        """

        :return:
        """
        raise NotImplementedError

    def add(self):
        """

        :return:
        """
        pass

    def replace(self, input):
        """

        :return:
        """
        pass
