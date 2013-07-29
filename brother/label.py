from brother.command import Command

class Label(object):
    
    commands = []
    
    def __init__(self, params):
        c = Command()
        self.commands.append(c.invalidate())
        self.commands.append(c.initialize())
        