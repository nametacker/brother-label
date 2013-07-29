class Command(object):
    
    def invalidate(self):
        return '\x00' * 200
    
    def initialize(self):
        return '\x1B' + ' \x40'