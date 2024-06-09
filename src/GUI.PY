import threading
from os import environ, path
import pygame
from Chess import Chess


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
        self.POS_SELECTED_COLOR = (185, 202, 66)

        #
        self.chess = Chess(1)
        current_path = path.dirname(__file__)
        self.icons = {

            "T1": pygame.image.load(
                path.join(current_path, 'icons', 'TW.png')),
            "C1": pygame.image.load(
                path.join(current_path, 'icons', 'CW.png')),
            "A1": pygame.image.load(
                path.join(current_path, 'icons', 'AW.png')),
            "R1": pygame.image.load(
                path.join(current_path, 'icons', 'RW.png')),
            "N1": pygame.image.load(
                path.join(current_path, 'icons', 'NW.png')),
            "P1": pygame.image.load(
                path.join(current_path, 'icons', 'PW.png')),
            "T2": pygame.image.load(
                path.join(current_path, 'icons', 'TB.png')),
            "P2": pygame.image.load(
                path.join(current_path, 'icons', 'PB.png')),
            "N2": pygame.image.load(
                path.join(current_path, 'icons', 'NB.png')),
            "C2": pygame.image.load(
                path.join(current_path, 'icons', 'CB.png')),
            "A2": pygame.image.load(
                path.join(current_path, 'icons', 'AB.png')),
            "R2": pygame.image.load(
                path.join(current_path, 'icons', 'RB.png'))
        }
        self.run()

    def calculateScreen(self):
        self.width_block = self.WIDTH/8
        # self.torre_white = pygame.transform.scale(self.torre_white, (50, 50))

    def mappingMatrizOnScreen(self):
        r = 0
        c = 0
        # mapeo la matriz en la pantalla recorriendo filas y
        # columnas y creando su correspondiente elemento
        for i in range(8):
            for j in range(8):
                elem = self.chess.globalGame[i][j]
                if (i+j+2) % 2 == 0:
                    pygame.draw.rect(self.screen, self.WHITE_COLOR,
                                     (c, r, self.width_block, self.width_block))
                else:
                    pygame.draw.rect(self.screen, self.GREEN_COLOR,
                                     (c, r, self.width_block, self.width_block))
                if (j == self.pos_selected[0] and i == self.pos_selected[1]):
                    pygame.draw.rect(self.screen,  self.POS_SELECTED_COLOR,
                                     (c, r, self.width_block, self.width_block))
                if elem != '  ':
                    self.screen.blit(self.icons[elem], (c+4, r+10))

                c += self.width_block
            r += self.width_block
            c = 0

    def run(self):
        environ['SDL_VIDEO_WINDOW_POS'] = '1'  # centrar ventana
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Proyecto 2 - IA - Inversed Chess')

        self.clock = pygame.time.Clock()
        self.running = True

        self.calculateScreen()
        self.pos_selected = [None, None]  # x, y
        on_press = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    on_press = True

            self.mappingMatrizOnScreen()

            current_position = pygame.mouse.get_pos()
            x = int(current_position[0]/self.width_block)
            y = int(current_position[1]/self.width_block)

            if on_press and pygame.mouse.get_pressed()[0]:
                on_press = False
                if (self.pos_selected[0] is not None and self.pos_selected[1] is not None):

                    if self.chess.globalGame[y][x][1] == '1' and self.chess.globalGame[y][x] != '  ':
                        self.pos_selected[0], self.pos_selected[1] = x, y
                    else:
                        if (self.pos_selected != [x, y]):
                            thread = threading.Thread(target=self.chess.run, args=(
                                self.pos_selected[0], self.pos_selected[1], x, y,))
                            thread.start()
                            self.pos_selected[0], self.pos_selected[1] = None, None
                else:
                    if self.chess.globalGame[y][x] != '  ':
                        self.pos_selected[0] = x
                        self.pos_selected[1] = y

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    gui = GUI(WIDTH, HEIGHT)
