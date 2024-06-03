import numpy as np
from Node import Node
import copy
from tabulate import tabulate
from os import system


testGamge = [
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', 'C1', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2'],
    ['T2', 'C2', 'A2', 'R2', 'N2', 'A2', 'C2', 'T2'],
]


class Chess:
    def __init__(self, humanPlayer) -> None:
        self.globalGame = [
            ['T1', 'C1', 'A1', 'R1', 'N1', 'A1', 'C1', 'T1'],
            ['P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1'],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2'],
            ['T2', 'C2', 'A2', 'R2', 'N2', 'A2', 'C2', 'T2'],
        ]
        # -1=MIN , 1=MAX
        self.humanPlayer = -1 if humanPlayer == 2 else 1
        self.deep_limit = 4

    def run(self):
        while True:
            system('cls')
            self.printGame(self.globalGame)
            yf, xf = input('ingrese la ficha a mover y,x: ').split(',')
            yf = int(yf)
            xf = int(xf)
            selected = self.globalGame[yf][xf]
            yd, xd = input('ingrese la posicion destino: ').split(',')
            yd = int(yd)
            xd = int(xd)
            self.globalGame[yd][xd] = selected
            self.globalGame[yf][xf] = '  '

            tree = self.generateTree()  # genero el arbol de juego
            node: Node = self.calculateMinimax(
                tree)  # obtengo la jugada minimax

            # remplazo el juego actual con el de la jugada minimax
            self.globalGame = copy.deepcopy(node.minimax)

            node = Node(self.globalGame, None, None, None, 0)
            node.isLeft()

            system('cls')
            if node.p1 == 0:
                self.printGame(self.globalGame)
                print('Gana jugador 1')
                break
            if node.p2 == 0:
                print('Gana jugador 2')
                self.printGame(self.globalGame)
                break

    def calculateMinimax(self, tree: list):
        while len(tree) != 1:

            nodeMaxDeep: Node = tree.pop()
            parent: Node = nodeMaxDeep.parent

            if (parent.type == 1):
                if (nodeMaxDeep.utility >= parent.utility):
                    parent.utility = nodeMaxDeep.utility
                    parent.minimax = nodeMaxDeep.game
            else:
                if (nodeMaxDeep.utility <= parent.utility):
                    parent.utility = nodeMaxDeep.utility
                    parent.minimax = nodeMaxDeep.game

        return tree[0]

    def generateTree(self):
        # auxiliares
        def generateChild(parent: Node, f, i, j, xi, yi):
            game = copy.deepcopy(parent.game)
            game[yi][xi] = f
            game[i][j] = '  '
            type = parent.type*-1

            utility = float(
                '-inf') if type == 1 else float('inf')

            return Node(game, parent, type, utility, parent.deep+1)

        # nodo inicial del juego actual / por defecto la maquina juega minimizando, player1 = MAX player2 = MIN
        initNode = Node(copy.deepcopy(self.globalGame),
                        None, self.humanPlayer*-1, self.humanPlayer*float('inf'), 0)

        queue = [initNode]  # generar los hijos por amplitud
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

                            if yi-direction >= 0 and yi-direction <= 7 and currentNode.game[yi-direction][xi] == '  ' and (i == 6 or i == 1):
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

                    # Alfir o Reina // DIAGONALES
                    if (ficha == f'A{player}' or ficha == f'N{player}'):
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

                    # Torre o Reina // verticales y horizontales
                    if (ficha == f'T{player}' or ficha == f'N{player}'):
                        movements = []
                        for k in range(1, 8):  # arriba
                            ya, xa = (i-k, j)
                            if (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                                if currentNode.game[ya][xa] != '  ':
                                    movements.append((ya, xa))
                                    break
                                else:
                                    movements.append((ya, xa))

                        for k in range(1, 8):  # abajo
                            ya, xa = (i+k, j)
                            if (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                                if currentNode.game[ya][xa] != '  ':
                                    movements.append((ya, xa))
                                    break
                                else:
                                    movements.append((ya, xa))
                        for k in range(1, 8):  # derecha
                            ya, xa = (i, j+k)
                            if (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                                if currentNode.game[ya][xa] != '  ':
                                    movements.append((ya, xa))
                                    break
                                else:
                                    movements.append((ya, xa))
                        for k in range(1, 8):  # izquierda
                            ya, xa = (i, j-k)
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

            # si hubo un nodo donde caputura alguna pieza descarto las que no, esto con el fin de obligarlo a capturar
            for child, wasCapture in moves:
                if wasCapture and hasCaptureMovements:
                    queue.append(child)
                    continue
                if not hasCaptureMovements:
                    queue.append(child)
        return tree

    def printGame(self, game):
        for i in range(0, 8):
            print(' '*2, i, end=' ')
        print()
        print(tabulate(game, tablefmt="simple_grid"))


chess = Chess(1)
chess.run()
