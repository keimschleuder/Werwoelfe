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
                print(playersNew[current].playerID, playersNew[current].role) # Testing only
                current = current + 1

    for _ in range(num - current):
        playersNew[current].setRole(Roles.DORFBEWOHNER.value)
        current = current + 1

    return playersNew

class Winners(Enum):
    DORFBEWOHNER = 0
    WEREWOLVES = 1
    WEISSER_WOLF = 2
    LOVERS = 3
    NONE = 4
    GAME_STILL_GOING = 5

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

class HexeActions(Enum):
    RETTEN = 0
    TOETEN = 1
    NICHTS = 2

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
        self.angeklagte = []
        self.hauptmann = None
        self.doWeisserWolf = False
        self.doAmor = True
        self.HexeHasKilled = False
        self.HexeHasHealed = False

    def findAllPlayersWithRole(self, roleID):
        playersWithRole = []
        for myPlayer in self.players:
            if myPlayer.role == roleID:
                playersWithRole.append(myPlayer)
        return playersWithRole

    def findPlayerByRole(self, roleID) -> Player:
        for myPlayer in self.players:
            if myPlayer.role == roleID:
                return myPlayer
        return None

    def joinGame(self, playerID):
        player = Player(playerID)
        self.players.append(player)

    def startGame(self):
        self.players = AssignRoles(self.players)

        self.werwoelfe = self.findAllPlayersWithRole(Roles.WERWOLF.value)
        self.weisserWolfPlayer = self.findPlayerByRole(Roles.WEISSER_WOLF.value)
        self.seherinPlayer = self.findPlayerByRole(Roles.SEHERIN.value)
        self.hexePlayer = self.findPlayerByRole(Roles.HEXE.value)
        self.amorPlayer = self.findPlayerByRole(Roles.AMOR.value)
        self.rabePlayer = self.findPlayerByRole(Roles.RABE.value)
        self.jaegerPlayers = self.findAllPlayersWithRole(Roles.JAEGER.value)
        self.banditPlayers = self.findAllPlayersWithRole(Roles.BANDIT.value)
        self.villagers = self.findAllPlayersWithRole(Roles.DORFBEWOHNER.value)

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
            if len(werewolvesCount) == 1 and werewolvesCount[0] == self.weisserWolfPlayer: # Nur noch der weisse Wolf lebt
                return Winners.WEISSER_WOLF.value
            else: # Werwoelfe haben gewonnen, auch wenn der weisse Wolf noch lebt, dieser hat dann verloren
                return Winners.WEREWOLVES.value
        if werewolvesCount == villagersCount == 0: # Nur Lover leben noch (Alle Tot ist schon ausgeschlossen)
            return Winners.LOVERS.value
        if werewolvesCount == loversCount == 0: # Nur Dorfbewohner leben noch
            return Winners.DORFBEWOHNER.value
        
        return Winners.GAME_STILL_GOING.value

    def playerById(self, targetID) -> Player:
        for myPlayer in self.players:
            if myPlayer.playerID == targetID:
                return myPlayer
        return None

    def exile(self, playerID: int, repeat = True):
        player = self.playerById(playerID)
        if player != None and player.playerState != PlayerState.DEAD.value:
            player.playerState = PlayerState.DEAD.value
            print(f"Killed Player with ID{player.playerID} and Role {player.role}")
            match player.role:
                case Roles.JAEGER.value:
                    try:
                        targetID = int(input("Which other player do you want to kill: "))
                        self.exile(targetID, repeat = True)
                    except:
                        print("Enter Valid Player ID")
                case Roles.BANDIT.value:
                    targets = [player.playerID + 1, player.playerID - 1]
                    for myTarget in targets:
                        self.exile(myTarget)
            if player.inLove and repeat:
                otherLover = self.lovers[0] if self.lovers.index(player) == 1 else self.lovers[1]
                self.exile(otherLover.playerID, repeat = False)

            winners = self.checkWin()

            return winners

    def nextCycle(self):
        self.state = self.state + 1

        # Logic for skipping cycles
        if (self.state == Cycle.AMOR.value and not self.doAmor) or (self.state == Cycle.AMOR.value and self.amorPlayer.playerState == PlayerState.DEAD.value):
            self.state = self.state + 1
        if self.state == Cycle.SEHERIN.value and self.seherinPlayer.playerState == PlayerState.DEAD.value:
            self.state = self.state + 1
        skip = True
        for myWerewolf in self.werwoelfe:
            if myWerewolf.playerState != PlayerState.DEAD.value:
                skip = False
        if self.state == Cycle.WERWOLF.value and skip:
            self.state = self.state + 1
        if (self.state == Cycle.WEISSER_WOLF.value and not self.doWeisserWolf) or (self.state == Cycle.WEISSER_WOLF.value and self.weisserWolfPlayer.playerState == PlayerState.DEAD.value):
            self.state = self.state + 1
            self.doWeisserWolf = True
        if self.state == Cycle.HEXE.value and self.hexePlayer.playerState == PlayerState.DEAD.value:
            self.state = self.state + 1
        if self.state == Cycle.RABE.value and self.rabePlayer.playerState == PlayerState.DEAD.value:
            self.state = self.state + 1
        if self.state == 7:
            self.state = Cycle.DAY.value

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
        try:
            print("Zeit für Anklagen")
            # Anklagen
            for myAngeklagte in self.angeklagte:
                print(myAngeklagte.playerID)
        finally:
            self.angeklagte.clear()
            self.nextCycle()

    def Amor(self):
        self.doAmor = False

        try:
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
        finally:
            self.nextCycle()
    def Seherin(self):
        try:
            targetID = int(input("ID of the Target: "))
            target = self.playerById(targetID)

            if target != None: 
                match target.playerState:
                    case PlayerState.GOOD.value:
                        print(PlayerState.GOOD.name)
                    case PlayerState.EVIL.value:
                        print(PlayerState.EVIL.name)
                    case PlayerState.DEAD.value:
                        print(PlayerState.DEAD.name)
                    case PlayerState.LOVER.value:
                        print(PlayerState.LOVER.name)
        finally:
            self.nextCycle()
    def Werwolf(self):
        self.victimID = None
        while self.victimID == None:
            victim = int(input("Wen sollen die Werwoelfe Toeten? "))
            if (self.playerById(victim) not in self.werwoelfe) and self.playerById(victim) != self.weisserWolfPlayer:
                self.victimID = victim

        self.nextCycle()
    def WeisserWolf(self):
        self.doWeisserWolf = False

        werewolves = []
        for myPlayer in self.players:
            if myPlayer.role == Roles.WERWOLF.value and myPlayer.playerState != PlayerState.DEAD.value:
                werewolves.append(myPlayer.playerID)

        if len(werewolves) > 0:
            print(f"You can Kill: {werewolves}")
            try:
                victim = int(input("Which one do you chose? (-1 for nobody): "))
            except:
                victim = -1

            if victim != -1 and victim in werewolves: # Can not kill Lovers
                self.exile(victim)
            else:
                print("Give a valid Player")
        else:
            print("No more Werewolves")

        self.nextCycle()
    def Hexe(self):
        additionalVictimID = None
        try:
            print(f"Opfer der Werwoelfe hat ID{self.victimID}")
            choice = int(input("Moechtest du retten (0)/jemand anderes toeten (1)/nichts tun (2)? "))
            match choice:
                case HexeActions.RETTEN.value:
                    if not self.HexeHasHealed:
                        self.victimID = None
                        self.HexeHasHealed = True
                case HexeActions.TOETEN.value:
                    if not self.HexeHasKilled:
                        additionalVictimID = int(input("Wen moechtest du zusaetzlich toeten?: "))
                        self.HexeHasKilled = True
        finally:
            if self.victimID != None:
                self.exile(self.victimID)
            if additionalVictimID != None:
                self.exile(additionalVictimID)
            
            self.nextCycle()
    def Rabe(self):
        try:       
            selectedPlayer = self.playerById(int(input("Do you know somebody suspicious?: ")))

            if selectedPlayer.playerState != PlayerState.DEAD.value:
                self.angeklagte.append(selectedPlayer)
        finally:    
            self.nextCycle()

# Testing
        
game = Game()

for i in range(16):
    game.joinGame(i)

game.startGame()