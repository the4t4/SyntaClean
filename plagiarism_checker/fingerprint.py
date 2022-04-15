class Fingerprint:
    def __init__(self, id, weight, node):
        self.id = id
        self.weight = weight
        self.node = node

    def __eq__(self, other):
        try:
            return self.weight == other.weight and self.node == other.node
        except AttributeError:
            return False
