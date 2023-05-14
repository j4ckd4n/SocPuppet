class Plugin:
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        raise NotImplementedError()