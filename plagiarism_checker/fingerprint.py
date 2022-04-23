class Fingerprint:
    def __init__(self, file, id, weight, node):
        self.file = file
        self.id = id
        self.weight = weight
        self.node = node

    def __eq__(self, other):
        try:
            return (self.file == self.file and 
                    self.id == other.id and 
                    self.weight == other.weight and 
                    self.node == other.node)
        except AttributeError:
            return False
    
    def __ne__(self, other):
        return not (self == other)
    
    def __repr__(self):
        return 'Fingerprint(%s, %d, %d, %r)' % (self.file, self.id, self.weight, self.node.data)
