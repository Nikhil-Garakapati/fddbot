from abc import ABCMeta, abstractmethod
class Entity(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

class Expression(Entity):
    
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Named(Entity):

    def __init__(self, name):
        self.name = name
        self.entries = []

    def create_entries(self,entries):
        for entry in entries:
            self.entries += [entry]

class Entry():

    def __init__(self, name, synonyms):
        self.name = name
        self.synonyms = synonyms
