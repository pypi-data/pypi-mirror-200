from pyaml_env import parse_config

class YamlParser(Parser):
    """ YamlParser  """
    def __init__(self, fpath):
        """

        :param fpath:
        """

        self.fpath = fpath
        self.data = self.load()

    def load(self):
        """

        :return:
        """
        data = parse_config(self.fpath, tag='!TAG')
        return data

    def save(self):
        """

        :return:
        """
        with open(self.fpath, 'w') as f:
            f.close()
