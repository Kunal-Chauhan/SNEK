from network import Client
from constants import State, Type
from typing import Tuple, List


class SNEKClient(Client):
    def __init__(self, players: List[Type.Grid]):
        super(SNEKClient, self).__init__()
        self.players = players

        (self.playerID, self.gameID), (start, end) = self.requestServer((State.init, players[0]))
        self.enemyID = (self.playerID+1) % 2
        for player in players:
            player["start"], player["end"] = start, end

        # the following represents the states of both the players in the game
        # state = (<player1 state>, <player2 state>)
        # for info about each state look up State class in constants.py
        self.state: Tuple[State, State] = State(), State()
        self.state[0].set(State.busy)
        self.state[1].set(State.busy) if self.playerID == 1 else self.state[1].set(State.waiting)

    def updatePlayers(self):
        packet = ((self.playerID, self.gameID), self.state[self.playerID].current, self.players[self.enemyID])
        msg = self.requestServer(packet)
        if msg:
            state, self.players[self.playerID] = msg
            if self.state[self.enemyID] != state:
                self.state[self.enemyID].set(state)
                if state == State.ready:
                    return True
        return False
