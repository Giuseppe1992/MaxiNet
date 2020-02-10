

class Mapper(object):
    def __init__(self, topo, physical_network_file):
        self.topo = topo
        self.physical_network_file = physical_network_file

    @staticmethod
    def check_valid_path(physical_network_file):
        pass


class EmbeddedGreedy(Mapper):
    pass


class EmbeddedPartitioned(Mapper):
    pass


class EmbeddedBalanced(Mapper):
    pass

