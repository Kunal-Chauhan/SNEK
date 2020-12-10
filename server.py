from network import Server
from constants import State, Type, Union, List, Dict, Tuple


class SNEKServer(Server):
    def __init__(self):
        super(SNEKServer, self).__init__()
        # {GameID: [ [State_player1, grid_player2], [State_player2, Grid_player1] ]}
        self.games: Dict[int, List[List[Union[Type.Grid]]]] = {}
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

        start, end = self.games[self.count][0][1]["start"], self.games[self.count][0][1]["end"]
        # NOTE:
        # here lastPlayer is not actually the index of last player but the current player
        # because it has been updated in the above if-else block
        return (self.lastPlayer, self.count), (start, end)

    # here, data: tuple[(playerID, gameID), State, enemy_grid]
    def processData(self, data, addr: Tuple[str, int]) -> Type.Basic:
        if data[-2] == State.init:
            return self.assignGame(data[-1])
        else:
            playerID, gameID = data[0]
            self.games[gameID][playerID] = data[1], data[-1]

            return self.games[gameID][(playerID+1) % 2]


if __name__ == '__main__':
    s = SNEKServer()
    s.run()
