from enum import Enum
import random
import Intro

doAmor = True

werewolves = [1, 1, 2, 2, 2, 3, 3, 4, 4]

def RoleCount(playersCount):
    count = []
    if werewolves[playersCount - 8] >= 3: # Weisser Wolf
        count.append(1)
    else:
        count.append(None)
    count.append(werewolves[playersCount - 8]) # Werevolves
    count.append(-1) # Dorfbewohner
    # Hexe, Seherin, Amor, Jaeger und Rabe
    for _ in range(5):
        count.append(1)

    return count

def AssignRoles(players: list):
    num = len(players)
    if num <= 7:
        return "Not enough players"
    elif num >= 16:
        return "Too many players"
    count = RoleCount(num)
    playersNew = []
    for _ in range(num):
        rand = random.randint(0, len(players) - 1)
        playersNew.append(players[rand])
        players.pop(rand)

    current = 0
    for i in range(len(count)):
        myCnt = count[i]
        if myCnt != None and myCnt != -1:
            for _ in range(myCnt):
                playersNew[current].setRole(i)
                current = current + 1

    for _ in range(num - current):
        playersNew[current].setRole(Roles.DORFBEWOHNER.value)
        current = current + 1

    return playersNew

class Roles(Enum):
    WEISSER_WOLF = 0
    WERWOLF = 1
    DORFBEWOHNER = 2
    HEXE = 3
    SEHERIN = 4
    AMOR = 5
    JAEGER = 6
    RABE = 7

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
    def __init__(self, id) -> None:
        self.playerID = id
        self.inLove = False
        self.loverIsOpponentTeam = False
        self.role = None
    
    def setRole(self, role):
        self.role = role
        if self.role >= 2:
            self.playerState = PlayerState.GOOD.value
        else:
            self.playerState = PlayerState.EVIL.value

class Game():
    def __init__(self) -> None:
        self.state = Cycle.AMOR.value
        self.players = []
        self.lovers = []
        self.hauptmann = None

    def nextCycle(self):
        self.state = self.state + 1
        if self.state == Cycle.AMOR.value and not doAmor:
            self.state = self.state + 1
        if self.state == 5:
            self.state = Cycle.DAY.value

    def Abstimmung(self):
        pass

    def Amor(self):
        self.doAmor = False
    def Seherin(self):
        pass
    def Werwolf(self):
        pass
    def Hexe(self):
        pass
        
# Testing only

myPlayers = []
for i in range(16):
    myPlayers.append(Player(i))

roles = AssignRoles(myPlayers)

print(f"Length: {len(roles)}")

for myRole in roles:
    match myRole.role:
        case Roles.WEISSER_WOLF.value:
            print(Roles.WEISSER_WOLF.name, myRole.playerID)
        case Roles.WERWOLF.value:
            print(Roles.WERWOLF.name, myRole.playerID)
        case Roles.DORFBEWOHNER.value:
            print(Roles.DORFBEWOHNER.name, myRole.playerID)
        case Roles.HEXE.value:
            print(Roles.HEXE.name, myRole.playerID)
        case Roles.SEHERIN.value:
            print(Roles.SEHERIN.name, myRole.playerID)
        case Roles.AMOR.value:
            print(Roles.AMOR.name, myRole.playerID)
        case Roles.JAEGER.value:
            print(Roles.JAEGER.name, myRole.playerID)
        case Roles.RABE.value:
            print(Roles.RABE.name, myRole.playerID)
