class detectabel:
    def __init__(self, size, location, team,*args, **kwargs):
        self.size = size
        self.location = location
        self.team = team


class structure(detectabel):
    def __init__ (self, helath):
        pass

class minion(detectabel):
    def __init__(self, u_type, health):
        self.type = u_type
        self.health = health

class champion(detectabel):
    def __init__ (self, health, name):
        self.health = health
        self.name = name


class monster(detectabel):
    def __init__(self, health, u_type):
        self.health = health
        self.type = u_type
