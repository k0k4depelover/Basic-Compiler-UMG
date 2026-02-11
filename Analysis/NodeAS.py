class NodeAS:
    def __init__(self, type, hijos=None, lineno=None):
        self.type = type 
        self.hijos = hijos if hijos is not None else []
        self.lineno = lineno

    def __repr__(self):
        return f"NodeAS(type='{self.type}', hijos={self.hijos}, line={self.lineno})"
