class Fingerprint:
    def __init__(self, id, weight, node):
        self.id = id
        self.weight = weight
        self.node = node

    def __eq__(self, other):
        try:
            return self.id == other.id and self.weight == other.weight and self.node == other.node
        except AttributeError:
            return False
    
    def __ne__(self, other):
        return not (self == other)
    
    def __repr__(self):
        return 'Fingerprint(%d, %d, %r)' % (self.id, self.weight, self.node.data)
