from network import Server
from constants import State, Type


class SNEKServer(Server):
    def __init__(self):
        super(SNEKServer, self).__init__()
        self.games: dict[int, list[list[int, Type.Grid]]] = {}
        self.count = 0
        self.lastPlayer = 0
        self.serverState: State = State()
        self.serverState.set(State.ready)

    def assignGame(self, data: Type.Grid):

        if self.serverState.current == State.ready:
            self.lastPlayer = 0
            self.count += 1
            self.games[self.count] = []
            self.games[self.count].append([State.busy, data])
            self.games[self.count].append([State.waiting, data.copy()])
            self.serverState.set(State.waiting)
        else:
            self.lastPlayer = 1
            self.games[self.count][1][0] = State.busy
            self.serverState.set(State.ready)

        # NOTE:
        # here lastPlayer is not actually the index of last player but the current player
        # because it has been updated in the above if-else block
        return self.lastPlayer, self.count

    # here, data: tuple[(playerID, gameID), State, player_grid]
    def processData(self, data, addr: tuple[str, int]) -> Type.Basic:
        if data[0] == State.init:
            return self.assignGame(data[-1])
        else:
            playerID = data[0][0]
            gameID = data[0][1]
            self.games[gameID][playerID] = data[1], data[-1]

            return self.games[gameID][(playerID+1) % 2]


if __name__ == '__main__':
    s = SNEKServer()
    s.run()
