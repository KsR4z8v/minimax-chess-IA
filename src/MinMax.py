import numpy as np
from Node import Node
import copy

from os import system


class Chess:
    def __init__(self) -> None:
        self.globalGame = [
            ['T1', 'C1', 'A1', '  ', 'N1', '  ', 'C1', 'T1'],
            ['P1', '  ', '  ', '  ', 'R1', '  ', 'P1', 'P1'],
            ['P1', '  ', 'P1', 'P1', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', 'P2', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', 'A1', '  '],
            ['  ', '  ', 'P2', 'P2', '  ', '  ', '  ', '  '],
            ['T2', 'C2', 'A2', 'R2', 'N2', '  ', '  ', 'T2'],
        ]

        self.humanPlayer = 1
        self.pcPlayer = 2
        self.deep_limit = 2

    def run(self):
        tree = self.generateTree()
        minimax = self.calculateMinimax(tree)
        self.globalGame = copy.deepcopy(minimax.game)
        print(minimax.type, minimax.utility, minimax.deep)
        self.printGame(self.globalGame)

    def calculateMinimax(self, tree: list):
        maxDeep = self.deep_limit
        while (len(tree) != 0 and maxDeep > 0):

            nodeMaxDeep: Node = None

            for i in range(0, len(tree)):
                if tree[i].deep == maxDeep:
                    nodeMaxDeep = tree.pop(i)
                    break

            if (nodeMaxDeep == None):
                maxDeep -= 1
                continue

            parent: Node = nodeMaxDeep.parent
            """             if nodeMaxDeep.utility != 0:
                print(f''''UTILIDAD:{nodeMaxDeep.utility} TIPO: {
                    nodeMaxDeep.type} PROFUNDIDAD: {nodeMaxDeep.deep}''''')
                self.printGame(nodeMaxDeep.game)
                system('pause') """
            if (parent.type == 1):
                if (nodeMaxDeep.utility > parent.utility):
                    parent.utility = nodeMaxDeep.utility
                    parent.minimax = nodeMaxDeep
            else:
                if (nodeMaxDeep.utility < parent.utility):
                    parent.utility = nodeMaxDeep.utility
                    parent.minimax = nodeMaxDeep

        return tree[0].minimax

    def generateTree(self):

        def generateChild(parent: Node, f, i, j, xi, yi):
            game = copy.deepcopy(parent.game)
            game[yi][xi] = f
            game[i][j] = '  '
            type = parent.type*-1

            utility = float(
                '-inf') if type == 1 else float('inf')

            """ if (parent.deep+1 == 1):
                self.printGame(game)
                system('pause') """
            return Node(game, parent, type, utility, parent.deep+1)

        initNode = Node(copy.deepcopy(self.globalGame),
                        None, -1, float('inf'), 0)

        queue = [initNode]
        tree = []

        while len(queue) != 0:
            currentNode: Node = queue.pop(0)
            tree.append(currentNode)
            # expando el nodo para saber si es un nodo hoja o si ya alcanzo el limite establecido
            if (currentNode.isLeft() or currentNode.deep == self.deep_limit):
                currentNode.calculateUtility()
                continue

            moves = []   # Genero todas las posibles jugadas del nodo actual tanto de captura como de movimiento
            hasCaptureMovements = False

            for i in range(0, 8):  # rows
                for j in range(0, 8):  # columns
                    ficha = currentNode.game[i][j]

                    player = 1 if currentNode.type == 1 else 2  # TURNO

                    if (ficha == f'P{player}'):  # peon
                        direction = (1 if player == 2 else -1)
                        # movimientos de captura
                        captureMoves = [(i-direction, j+1), (i-direction, j-1)]

                        for yi, xi in captureMoves:
                            if ((yi >= 0 and yi <= 7 and xi >= 0 and xi <= 7) and currentNode.game[yi][xi][1] == str(2 if player == 1 else 1)):
                                hasCaptureMovements = True
                                moves.append((generateChild(
                                    currentNode, ficha, i, j, xi, yi), True))
                        yi = i-direction
                        xi = j
                        # movimientos basicos del peon
                        if (yi >= 0 and yi <= 7 and currentNode.game[yi][xi] == '  '):
                            moves.append((generateChild(
                                currentNode, ficha, i, j, xi, yi), False))

                            if currentNode.game[yi-direction][xi] == '  ' and (i == 6 or i == 1):
                                moves.append((generateChild(
                                    currentNode, ficha, i, j, xi, yi - direction), False))

                    if (ficha == f'C{player}'):  # caballo
                        movements = [(i-2, j+1), (i-2, j-1),
                                     (i+2, j+1), (i+2, j-1), (i-1, j+2), (i-1, j-2), (i+1, j+2), (i+1, j-2)]
                        for yi, xi in movements:
                            if yi >= 0 and yi <= 7 and xi <= 7 and xi >= 0:
                                if (currentNode.game[yi][xi][1] == str(player)):
                                    continue

                                isCapture = False
                                if currentNode.game[yi][xi][1] != str(player) and currentNode.game[yi][xi] != '  ':
                                    hasCaptureMovements = True
                                    isCapture = True

                                moves.append((generateChild(
                                    currentNode, ficha, i, j, xi, yi), isCapture))

                    if (ficha == f'R{player}'):  # REY
                        movements = [(i+1, j), (i-1, j), (i, j+1), (i, j-1),
                                     (i+1, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1)]
                        for yi, xi in movements:
                            if yi <= 7 and yi >= 0 and xi >= 0 and xi <= 7:
                                if (currentNode.game[yi][xi][1] == str(player)):
                                    continue
                                isCapture = False
                                if (currentNode.game[yi][xi][1] != str(player) and currentNode.game[yi][xi] != '  '):
                                    isCapture = True
                                    hasCaptureMovements = True
                                moves.append((generateChild(
                                    currentNode, ficha, i, j, xi, yi), isCapture))

                    if (ficha == f'A{player}'):  # Alfir
                        movements = []
                        for k in range(1, 8):  # diagonal superior derecha
                            ya, xa = (i-k, j+k)
                            if (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                                if currentNode.game[ya][xa] != '  ':
                                    movements.append((ya, xa))
                                    break
                                else:
                                    movements.append((ya, xa))

                        for k in range(1, 8):  # diagonal superior izquierda
                            ya, xa = (i-k, j-k)
                            if (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                                if currentNode.game[ya][xa] != '  ':
                                    movements.append((ya, xa))
                                    break
                                else:
                                    movements.append((ya, xa))
                        for k in range(1, 8):  # diagonal inferior derecha
                            ya, xa = (i+k, j+k)
                            if (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                                if currentNode.game[ya][xa] != '  ':
                                    movements.append((ya, xa))
                                    break
                                else:
                                    movements.append((ya, xa))
                        for k in range(1, 8):  # diagonal inferior izquierda
                            ya, xa = (i+k, j-k)
                            if (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                                if currentNode.game[ya][xa] != '  ':
                                    movements.append((ya, xa))
                                    break
                                else:
                                    movements.append((ya, xa))

                        for yi, xi in movements:
                            if yi <= 7 and yi >= 0 and xi >= 0 and xi <= 7:
                                if currentNode.game[yi][xi][1] == str(player):
                                    continue
                                isCapture = False
                                if (currentNode.game[yi][xi][1] != str(player) and currentNode.game[yi][xi] != '  '):
                                    isCapture = True
                                    hasCaptureMovements = True
                                moves.append((generateChild(
                                    currentNode, ficha, i, j, xi, yi), isCapture))

            # si hubo un nodo donde caputura alguna pieza filtro las que no, esto con el fin de obligarlo a capturar
            for child, wasCapture in moves:
                if wasCapture and hasCaptureMovements:
                    queue.append(child)
                    continue
                if not hasCaptureMovements:
                    queue.append(child)

        return tree

    def printGame(self, game):
        for i in range(0, 8):
            print(i, end=' | ')
            for j in range(0, 8):
                print(game[i][j], end='')

            print()


chess = Chess()
chess.run()
