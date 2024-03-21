from enum import Enum

doAmor = True

class Roles(Enum):
    WERWOLF = 0
    DORFBEWOHNER = 1
    HEXE = 2
    SEHERIN = 3
    AMOR = 4
    JAEGER = 5

class Cycle(Enum):
    DAY = 0
    AMOR = 1
    SEHERIN = 2
    WERWOLF = 3
    HEXE = 4

class PlayerState(Enum):
    GOOD = 0
    EVIL = 1
    DEAD = 2
    GOOD_LOVER = 3
    EVIL_LOVER = 4

class Player():
    def __init__(self, id, role: Roles) -> None:
        self.playerID = id
        self.inLove = False
        self.loverIsOpponentTeam = False
        self.role = role
        if self.role >= 1:
            self.playerState = PlayerState.GOOD
        else:
            self.playerState = PlayerState.EVIL

class Game():
    def __init__(self) -> None:
        self.state = Cycle.AMOR
        self.players = []

    def nextCycle(self):
        self.state = self.state + 1
        if self.state == Cycle.AMOR and not doAmor:
            self.state = self.state + 1
        if self.state == 5:
            self.state = Cycle.DAY

    def Abstimmung(self):
        pass

    def Amor(self):
        pass
    def Seherin(self):
        pass
    def Werwolf(self):
        pass
    def Hexe(self):
        pass
        
