import numpy as np
from Node import Node
import copy
from tabulate import tabulate
from os import system
from time import sleep


test1 = [
    ['  ', '  ', '  ', 'C1', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2'],
    ['T2', 'C2', 'A2', 'R2', 'N2', 'A2', 'C2', 'T2'],
]


test2 = [
    ['  ', '  ', '  ', '  ', '  ', 'A1', '  ', 'T1'],
    ['  ', '  ', '  ', '  ', 'R1', '  ', '  ', 'P1'],
    ['P1', '  ', '  ', 'P1', '  ', 'P1', '  ', 'P1'],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['P2', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', 'C1', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
]


class Chess:
    def __init__(self, humanPlayer) -> None:
        self.init_game = [
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
        self.deep_limit = 5
        self.time_line = [self.init_game]

    def run(self, x0, y0, x1, y1, callbackMessage):

        selfMoves = list()
        mustCapture = self.generateChilds(selfMoves,
                                          Node(self.time_line[-1], None, 1, 0, 0))
        aux = copy.deepcopy(self.time_line[-1])
        ficha = self.time_line[-1][y0][x0]
        aux[y0][x0] = '  '
        aux[y1][x1] = ficha
        isValid = False
        for child in selfMoves:
            if aux == child.game:
                isValid = True
                break
        if not isValid:
            if (mustCapture):
                return callbackMessage('Debes capturar')
            return
        self.time_line.append(aux)
        # genero la desicion minimax
        node: Node = self.minimax(-1,
                                  copy.deepcopy(self.time_line[-1]), self.deep_limit)

        if (node.minimax is None):  # si no hubo desicion minimax evaluo si hubo un ganador
            self.time_line.append(node.minimax)
            if node.p1 < node.p2:
                callbackMessage('Gana jugador 1')
            elif node.p1 > node.p2:
                callbackMessage('Gana jugador 2')
            else:
                callbackMessage('Empate')
            self.restart()
        else:
            self.time_line.append(node.minimax)
            node.game = node.minimax
            node.isLeft()
            if node.p1 == 0:
                callbackMessage('Gana jugador 1')
                self.restart()
            if node.p2 == 0:
                callbackMessage('Gana jugador 2')
                self.restart()
    # funcion auxiliar que crea un nodo y lo retorna

    def restart(self):
        while len(self.time_line) != 1:
            self.time_line.pop()
            sleep(0.01)

    def revert(self):
        if len(self.time_line) < 3:
            return
        self.time_line.pop()
        self.time_line.pop()
        self.globalGame = self.time_line[len(self.time_line)-1]

    def createChild(self, parent: Node, ficha, i, j, xi, yi):
        game = copy.deepcopy(parent.game)
        game[yi][xi] = ficha
        game[i][j] = '  '
        type: int = parent.type*-1
        """ self.printGame(game)
        system('pause') """
        utility = float(
            '-inf') if type == 1 else float('inf')
        return Node(game, parent, type, utility, parent.deep+1)

    # funcion auxiliar para generar los hijos dado una lista de coordenadas
    def coordinates_to_childs(self, moves, coordinates, i, j, node: Node, playerTurn):
        for yi, xi in coordinates:
            if not (yi <= 7 and yi >= 0 and xi >= 0 and xi <= 7):
                continue

            if node.game[yi][xi][1] == str(playerTurn):
                continue
            isCapture = False
            if (node.game[yi][xi][1] != str(playerTurn) and node.game[yi][xi] != '  '):
                moves[0] = True
                isCapture = True
            moves[1].append((self.createChild(
                node, node.game[i][j], i, j, xi, yi), isCapture))

    # Movmientos PEONES
    def generate_movements_pawn(self, moves, node: Node, playerTurn, i, j):
        direction = (1 if playerTurn == 2 else -1)
        # movimientos de captura
        captureCoordinates = [(i-direction, j+1), (i-direction, j-1)]
        for yi, xi in captureCoordinates:
            if ((yi >= 0 and yi <= 7 and xi >= 0 and xi <= 7) and node.game[yi][xi][1] == str(2 if playerTurn == 1 else 1)):
                moves[0] = True
                moves[1].append((self.createChild(
                    node, node.game[i][j], i, j, xi, yi), True))
        yi = i-direction
        xi = j
        # movimientos basicos del peon
        if (yi >= 0 and yi <= 7 and node.game[yi][xi] == '  '):
            if yi == 0 or yi == 7:  # si llego a un extremo para reclamar una ficha
                toReclaimn = ['A', 'C', 'T', 'R', 'N']
                for f in toReclaimn:
                    moves[1].append((self.createChild(
                        node, f+str(playerTurn), i, j, xi, yi), False))
            else:
                moves[1].append((self.createChild(
                    node, node.game[i][j], i, j, xi, yi), False))
            # si esta en la linea inicial para avanzar 2 casillas
            if yi-direction >= 0 and yi-direction <= 7 and node.game[yi-direction][xi] == '  ' and (i == 6 or i == 1):
                moves[1].append((self.createChild(
                    node, node.game[i][j], i, j, xi, yi - direction), False))

    # Movmientos CABALLO
    def generate_movements_hourse(self, moves, node: Node, playerTurn, i, j):
        coordinates = [(i-2, j+1), (i-2, j-1),
                       (i+2, j+1), (i+2, j-1), (i-1, j+2), (i-1, j-2), (i+1, j+2), (i+1, j-2)]
        self.coordinates_to_childs(moves, coordinates, i,
                                   j, node, playerTurn)

    # movimientos en CRUZ
    def generate_movements_cross(self, moves, node: Node, playerTurn, i, j, max_step):
        coordinates = []
        for k in range(1, max_step):  # arriba
            ya, xa = (i-k, j)
            if not (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                break
            if node.game[ya][xa] != '  ':
                coordinates.append((ya, xa))
                break
            else:
                coordinates.append((ya, xa))
        for k in range(1, max_step):  # abajo
            ya, xa = (i+k, j)
            if not (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                break
            if node.game[ya][xa] != '  ':
                coordinates.append((ya, xa))
                break
            else:
                coordinates.append((ya, xa))
        for k in range(1, max_step):  # derecha
            ya, xa = (i, j+k)
            if not (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                break
            if node.game[ya][xa] != '  ':
                coordinates.append((ya, xa))
                break
            else:
                coordinates.append((ya, xa))
        for k in range(1, max_step):  # izquierda
            ya, xa = (i, j-k)
            if not (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                break
            if node.game[ya][xa] != '  ':
                coordinates.append((ya, xa))
                break
            else:
                coordinates.append((ya, xa))
        self.coordinates_to_childs(moves, coordinates, i,
                                   j, node, playerTurn)

    # movimientos en CRUZ
    def generate_movements_diagonals(self, moves, node: Node, playerTurn, i, j, max_step):
        coordinates = []
        for k in range(1, max_step):  # diagonal superior derecha
            ya, xa = (i-k, j+k)
            if not (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                break
            if node.game[ya][xa] != '  ':
                coordinates.append((ya, xa))
                break
            else:
                coordinates.append((ya, xa))

        for k in range(1, max_step):  # diagonal superior izquierda
            ya, xa = (i-k, j-k)
            if not (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                break
            if node.game[ya][xa] != '  ':
                coordinates.append((ya, xa))
                break
            else:
                coordinates.append((ya, xa))

        for k in range(1, max_step):  # diagonal inferior derecha
            ya, xa = (i+k, j+k)
            if not (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                break
            if node.game[ya][xa] != '  ':
                coordinates.append((ya, xa))
                break
            else:
                coordinates.append((ya, xa))

        for k in range(1, max_step):  # diagonal inferior izquierda
            ya, xa = (i+k, j-k)
            if not (ya <= 7 and ya >= 0 and xa >= 0 and xa <= 7):
                break
            if node.game[ya][xa] != '  ':
                coordinates.append((ya, xa))
                break
            else:
                coordinates.append((ya, xa))
        self.coordinates_to_childs(moves, coordinates, i,
                                   j, node, playerTurn)

    def generateChilds(self, stack, currentNode: Node):
        # Genero todas las posibles jugadas del nodo actual tanto de captura como de movimiento
        moves = [False, []]
        playerTurn = 1 if currentNode.type == 1 else 2  # TURNO
        for i in range(0, 8):  # rows
            for j in range(0, 8):  # columns
                ficha = currentNode.game[i][j]
                if (ficha == f'P{playerTurn}'):  # peon
                    self.generate_movements_pawn(
                        moves, currentNode, playerTurn, i, j)
                if (ficha == f'C{playerTurn}'):  # caballo
                    self.generate_movements_hourse(
                        moves, currentNode, playerTurn, i, j)
                if (ficha == f'A{playerTurn}'):  # Alfir
                    self.generate_movements_diagonals(
                        moves, currentNode, playerTurn, i, j, 8)
                if (ficha == f'R{playerTurn}'):  # REY
                    self.generate_movements_cross(
                        moves, currentNode, playerTurn, i, j, 2)
                    self.generate_movements_diagonals(
                        moves, currentNode, playerTurn, i, j, 2)
                if (ficha == f'T{playerTurn}'):  # TORRE
                    self.generate_movements_cross(
                        moves, currentNode, playerTurn, i, j, 8)
                if (ficha == f'N{playerTurn}'):  # REYNA
                    self.generate_movements_cross(
                        moves, currentNode, playerTurn, i, j, 8)
                    self.generate_movements_diagonals(
                        moves, currentNode, playerTurn, i, j, 8)

        # si hubo alguna captura filtro las jugadas donde solo se captura esto para obligar a capturar
        for child, wasCapture in moves[1]:
            if wasCapture and moves[0]:
                stack.append(child)
                currentNode.totalChilds += 1
                continue
            if not moves[0]:
                currentNode.totalChilds += 1
                stack.append(child)
        return moves[0]

    def minimax(self, player_minimax, game_state, deep_limit) -> Node:
        # nodo inicial del juego actual / por defecto la maquina juega minimizando, player1 = MAX player2 = MIN
        initNode = Node(game_state, None, player_minimax, -
                        1*player_minimax*float('inf'), 0)
        stack = [initNode]  # generar los hijos por profundidad
        while len(stack) != 0:
            currentNode: Node = stack.pop()
            currentNode.heredateIntervale()

            if (currentNode.alfa >= currentNode.beta):
                currentNode.parent.informeUtility()
                continue
            # verifico si  el nodo es un nodo hoja o si ya alcanzo el limite establecido
            if (currentNode.isLeft() or currentNode.deep == deep_limit):
                currentNode.calculateUtility()
                continue
            self.generateChilds(stack, currentNode)

            # si no tiene hijos significa que no tiene mas jugadas por lo tanto calculo su utilidad
            if (currentNode.totalChilds == 0):
                currentNode.calculateUtility()

            """ print(initNode.alfa, initNode.beta,
                  initNode.totalChilds, initNode.totalChildChecks) """

        return initNode

    def printGame(self, game):
        for i in range(0, 8):
            print(' '*2, i, end=' ')
        print()
        print(tabulate(game, tablefmt="simple_grid"))
