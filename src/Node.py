class Node:
    def __init__(self, game: list, parent, type, utility, deep) -> None:
        self.game = game
        self.parent: Node = parent
        self.type = type
        self.deep = deep
        self.utility = utility
        self.minimax = None  # guardo el estado del tablero con la desicion minimax tomada
        self.p1 = 0  # Puntaje jugador 1 // total de fichas de player 1
        self.p2 = 0  # Puntaje jugador 2 // total de fichas de player 2
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.totalChilds = 0
        self.totalChildChecks = 0

    def isLeaf(self):  # se calcula que pasa en el nodo y se guarda el puntaje de cada jugador que seria el numero de fichas de cada uno
        self.p1 = 0
        self.p2 = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if (self.game[i][j][1] == '1'):
                    self.p1 += 1
                elif self.game[i][j][1] == '2':
                    self.p2 += 1
        return self.p1 == 0 or self.p2 == 0

    def heredateIntervale(self):
        if (self.parent is None):
            return
        self.alfa = self.parent.alfa
        self.beta = self.parent.beta

    def calculateUtility(self):
        if self.p2 == 0:
            self.utility = float('-inf')
        elif self.p1 == 0:
            self.utility = float('inf')
        else:
            if (self.type == 1):  # en caso de que sea un nodo tipo MAX
                self.utility = (16-self.p1) + self.p2
            else:
                self.utility = -((16-self.p2) + self.p1)

        self.informUtility()
        return self.utility

    def informUtility(self):
        if self.parent is None:
            return
        if (self.parent.type == 1 and self.utility >= self.parent.utility):  # MAX
            self.parent.utility = self.utility
            self.parent.alfa = self.utility
            self.parent.minimax = self.game

        if (self.parent.type == -1 and self.utility <= self.parent.utility):  # MIN
            self.parent.utility = self.utility
            self.parent.beta = self.utility
            self.parent.minimax = self.game

        self.parent.totalChildChecks += 1

        if self.parent.totalChilds == self.parent.totalChildChecks:
            self.parent.informUtility()
