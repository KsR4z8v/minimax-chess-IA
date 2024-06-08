import pygame
from os import environ, path
from Chess import Chess

import threading
"""
Autores:
Oscar Fernando Rivera Pardo 
Jose David Suarez Cardona
Jeferson Aguiar Dominguez
"""


WIDTH = 600
HEIGHT = 600


class GUI:
    def __init__(self, width, heigth) -> None:
        # constantes
        self.WIDTH = width
        self.HEIGHT = heigth

        self.WHITE_COLOR = (231, 233, 209)
        self.GREEN_COLOR = (122, 146, 89)

        #
        self.chess = Chess(1)

        self.TB = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'TB.png'))

        self.TW = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'TW.png'))

        self.PB = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'PB.png'))

        self.PW = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'PW.png'))

        self.NW = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'NW.png'))

        self.NB = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'NB.png'))

        self.CW = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'CW.png'))

        self.CB = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'CB.png'))

        self.AW = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'AW.png'))

        self.AB = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'AB.png'))

        self.RW = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'RW.png'))

        self.RB = pygame.image.load(
            path.join(path.dirname(__file__), 'icons', 'RB.png'))
        self.run()

    def calculateScreen(self):
        self.width_block = self.WIDTH/8
        """ self.torre_white = pygame.transform.scale(self.torre_white, (50, 50)) """

    def mappingMatrizOnScreen(self):

        r = 0
        c = 0
        # mapeo la matriz en la pantalla recorriendo filas y columnas y creando su correspondiente elemento
        for i in range(8):
            for j in range(8):
                elem = self.chess.globalGame[i][j]
                if ((i+j+2) % 2 == 0):
                    pygame.draw.rect(self.screen, self.WHITE_COLOR,
                                     (c, r, self.width_block, self.width_block))
                else:
                    pygame.draw.rect(self.screen, self.GREEN_COLOR,
                                     (c, r, self.width_block, self.width_block))
                if (elem == 'T1'):
                    self.screen.blit(self.TW, (c+4, r+10))

                if (elem == 'P1'):
                    self.screen.blit(self.PW, (c+4, r+6))

                if (elem == 'N1'):
                    self.screen.blit(self.NW, (c+4, r+6))

                if (elem == 'C1'):
                    self.screen.blit(self.CW, (c+4, r+6))

                if (elem == 'A1'):
                    self.screen.blit(self.AW, (c+4, r+6))

                if (elem == 'R1'):
                    self.screen.blit(self.RW, (c+4, r+6))

                if (elem == 'T2'):
                    self.screen.blit(self.TB, (c+4, r+10))

                if (elem == 'P2'):
                    self.screen.blit(self.PB, (c+4, r+6))

                if (elem == 'N2'):
                    self.screen.blit(self.NB, (c+4, r+6))

                if (elem == 'C2'):
                    self.screen.blit(self.CB, (c+4, r+6))

                if (elem == 'A2'):
                    self.screen.blit(self.AB, (c+4, r+6))

                if (elem == 'R2'):
                    self.screen.blit(self.RB, (c+4, r+6))

                c += self.width_block
            r += self.width_block
            c = 0

    def initAlgorithm(self):
        pass

    def run(self):
        environ['SDL_VIDEO_WINDOW_POS'] = '1'  # centrar ventana
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Proyecto 2 - IA - Inversed Chess')

        self.clock = pygame.time.Clock()
        self.running = True

        self.calculateScreen()
        movement = list()
        onPress = True
        while self.running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    self.running = False

                if (event.type == pygame.MOUSEBUTTONUP):
                    onPress = True

            self.mappingMatrizOnScreen()

            current_position = pygame.mouse.get_pos()
            x = int(current_position[0]/self.width_block)
            y = int(current_position[1]/self.width_block)

            if onPress and pygame.mouse.get_pressed()[0]:

                onPress = False

                movement.append((x, y))
                if len(movement) == 2:

                    h1 = threading.Thread(
                        target=self.chess.run, args=(movement[0][0], movement[0][1], movement[1][0], movement[1][1],))
                    h1.start()
                    movement.clear()
                elif (self.chess.globalGame[movement[0][1]][movement[0][0]] == '  '):
                    movement.clear()

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        exit()


if __name__ == '__main__':
    gui = GUI(WIDTH, HEIGHT)
