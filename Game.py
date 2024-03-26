from enum import Enum
import random
import Intro

doAmor = True

werewolves = [1, 1, 2, 2, 2, 3, 3, 4, 4]

def RoleCount(playersCount):
    count = []
    if werewolves[playersCount - 8] >= 3: # Weisser Wolf
        count.append(1)
        count.append(werewolves[playersCount - 8] - 1) # Werevolves
    else:
        count.append(None)
        count.append(werewolves[playersCount - 8]) # Werevolves
    count.append(-1) # Dorfbewohner
    # Hexe, Seherin, Amor, Jaeger, Rabe und Bandit
    for _ in range(6):
        count.append(1)

    # More passive Roles
    if playersCount >= 14:
        count[Roles.JAEGER.value] = count[Roles.JAEGER.value] + 2
        count[Roles.BANDIT.value] = count[Roles.BANDIT.value] + 2
    elif playersCount >= 12:
        count[Roles.JAEGER.value] = count[Roles.JAEGER.value] + 1
        count[Roles.BANDIT.value] = count[Roles.BANDIT.value] + 1

    return count

def AssignRoles(players: list):
    num = len(players)
    if num < 8:
        return "Not enough players"
    elif num > 16:
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

class Winners(Enum):
    DORFBEWOHNER = 0
    WEREWOLVES = 1
    LOVERS = 2
    NONE = 3
    GAME_STILL_GOING = 4

class Roles(Enum):
    WEISSER_WOLF = 0
    WERWOLF = 1
    DORFBEWOHNER = 2
    HEXE = 3
    SEHERIN = 4
    AMOR = 5
    JAEGER = 6
    RABE = 7
    BANDIT = 8

class Cycle(Enum):
    DAY = 0
    AMOR = 1
    SEHERIN = 2
    WERWOLF = 3
    WEISSER_WOLF = 4
    HEXE = 5
    RABE = 6

class PlayerState(Enum):
    GOOD = 0
    EVIL = 1
    DEAD = 2
    LOVER = 3 # Nur, wenn Lover ein eigenes TEam sind

class Player():
    def __init__(self, id) -> None:
        self.playerID = id
        self.inLove = False
        self.loverIsOpponentTeam = False
        self.role = None
        self.playerState = None
    
    def setRole(self, role: int):
        self.role = role
        if self.role >= 2:
            self.playerState = PlayerState.GOOD.value
        else:
            self.playerState = PlayerState.EVIL.value

class Game():
    def __init__(self) -> None:
        self.state = Cycle.DAY.value
        self.players = []
        self.lovers = []
        self.hauptmann = None
        self.doWeisserWolf = False
        self.doAmor = True

    def joinGame(self, playerID):
        player = Player(playerID)
        self.players.append(player)

    def startGame(self):
        self.players = AssignRoles(self.players)
        self.nextCycle()

    def checkWin(self):
        aliveWerewolves = []
        aliveVillagers = []
        deadPlayers = []
        loversAreAlive = False
        for myPlayer in self.players:
            match myPlayer.playerState:
                case PlayerState.GOOD.value:
                    aliveVillagers.append(myPlayer)
                case PlayerState.EVIL.value:
                    aliveWerewolves.append(myPlayer)
                case PlayerState.DEAD.value:
                    deadPlayers.append(myPlayer)
                case PlayerState.LOVER.value:
                    loversAreAlive = True

        werewolvesCount = len(aliveWerewolves)
        villagersCount = len(aliveVillagers)
        deadCount = len(deadPlayers)
        playerCount = len(self.players)
        loversCount = loversAreAlive + loversAreAlive

        if deadCount == playerCount: # Alle Tot
            return Winners.NONE.value
        if werewolvesCount > villagersCount + loversCount: # Werwoelfe sind in der Ueberzahl
            return Winners.WEREWOLVES.value
        if werewolvesCount == villagersCount == 0: # Nur Lover leben noch (Alle Tot ist schon ausgeschlossen)
            return Winners.LOVERS.value
        if werewolvesCount == loversCount == 0: # Nur Dorfbewohner leben noch
            return Winners.DORFBEWOHNER.value
        
        return Winners.GAME_STILL_GOING.value

    def playerById(self, targetID):
        for myPlayer in self.players:
            if myPlayer.playerID == targetID:
                return myPlayer

    def exile(self, playerID, repeat = True):
        player = self.playerById(playerID)
        if player != None:
            player.playerState = PlayerState.DEAD.value
            match player.role:
                case Roles.JAEGER.value:
                    targetID = player.playerID + 1
                    self.exile(targetID)
                case Roles.BANDIT.value:
                    targets = [player.playerID + 1, player.playerID - 1]
                    for myTarget in targets:
                        self.exile(myTarget)
            if player in self.lovers and repeat:
                otherLover = self.lovers[0] if self.lovers.index(player) == 1 else self.lovers[1]
                self.exile(otherLover, repeat = False)

            winners = self.checkWin()

            return winners

    def nextCycle(self):
        self.state = self.state + 1
        if self.state == Cycle.AMOR.value and not self.doAmor:
            self.state = self.state + 1
        if self.state == 6:
            self.state = Cycle.DAY.value
        if self.state == Cycle.WEISSER_WOLF.value and not self.doWeisserWolf :
            self.state = self.state + 1

        match self.state:
            case Cycle.DAY.value:
                self.Abstimmung()
            case Cycle.AMOR.value:
                self.Amor()
            case Cycle.SEHERIN.value:
                self.Seherin()
            case Cycle.WERWOLF.value:
                self.Werwolf()
            case Cycle.WEISSER_WOLF.value:
                self.WeisserWolf()
            case Cycle.HEXE.value:
                self.Hexe()
            case Cycle.RABE.value:
                self.Rabe()

    def Abstimmung(self):
        self.nextCycle()

    def Amor(self):
        self.doAmor = False

        # Let the Amor select two Roles
        lover1 = self.playerById(int(input("ID of Lover 1: ")))
        lover2 = self.playerById(int(input("ID of Lover 2: ")))

        self.lovers = [lover1, lover2]

        if lover1.playerState != lover2.playerState:
            self.loversAreTeirOwnTeam = True
            for myLover in self.lovers:
                myLover.playerState = PlayerState.LOVER.value
        else:
            self.loversAreTeirOwnTeam = False

        for myLover in self.lovers:
            myLover.inLove = True

        if self.loversAreTeirOwnTeam:
            print(f"Lovers ID{lover1.playerID} and ID{lover2.playerID} are opponents")
        else:
            print(f"Lovers ID{lover1.playerID} and ID{lover2.playerID} are on the same team")

        self.nextCycle()
    def Seherin(self):
        targetID = int(input("ID of the Target: "))
        target = self.playerById(targetID)
        
        print(target.playerState)

        self.nextCycle()
    def Werwolf(self):
        self.nextCycle()
    def WeisserWolf(self):
        self.nextCycle()
    def Hexe(self):
        self.nextCycle()
    def Rabe(self):
        self.nextCycle()

# Testing
        
game = Game()

for i in range(16):
    game.joinGame(i)

game.startGame()