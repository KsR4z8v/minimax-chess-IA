class Node:
    def __init__(self, game: list, parent, type, utility, deep) -> None:
        self.game = game
        self.parent = parent
        self.type = type
        self.deep = deep
        self.utility = utility
        self.minimax: Node = None  # guardo el nodo de la desicion minimax tomada
        self.p1 = 0  # total de ficas de player 1
        self.p2 = 0  # total de fichas de player 2

    def isLeft(self):  # se calcula que pasa en el nodo
        for i in range(0, 8):
            for j in range(0, 8):
                if (self.game[i][j][1] == '1'):
                    self.p1 += 1
                elif self.game[i][j][1] == '2':
                    self.p2 += 1
        return self.p1 == 0 or self.p2 == 0

    def calculateUtility(self):
        if (self.type == 1):  # en caso de que sea un nodo tipo MAX
            self.utility = 16-self.p1
        else:  # en caso de que sea un nodo tipo MIN
            self.utility = -(16-self.p2)

        return self.utility
