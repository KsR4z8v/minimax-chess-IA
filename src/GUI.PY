import threading
from os import environ, path
import pygame
from Chess import Chess
from time import sleep

WIDTH = 600
HEIGHT = 600


class GUI:
    def __init__(self, width, heigth) -> None:
        # constantes
        self.WIDTH = width
        self.HEIGHT = heigth

        self.WHITE_COLOR = (231, 233, 209)
        self.GREEN_COLOR = (122, 146, 89)
        self.BROWN_COLOR = (116, 76, 52)
        self.BLACK_COLOR = (32, 27, 24)
        self.BACKGROUND_COLOR = (50, 46, 43)
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

    def infoModal(self, screen, text):
        width_y = 130
        width_x = 300
        x = (self.WIDTH/2) - width_x/2
        y = (self.HEIGHT/2) - width_y/2

        z = pygame.draw.rect(screen, self.BACKGROUND_COLOR,
                             (x, y, width_x, width_y), border_bottom_left_radius=15, border_bottom_right_radius=15,
                             border_top_left_radius=15, border_top_right_radius=15)
        font = pygame.font.SysFont('Verdana', 20)
        size = font.size(text)
        screen.blit(font.render(text, 1, self.WHITE_COLOR),
                    (x+(width_x/2)-size[0]/2, y+(width_y/2)-size[1]/2))
        self.infoModalActive = True

    def mappingMatrizOnScreen(self, screen):
        r = 0
        c = 0
        # mapeo la matriz en la pantalla recorriendo filas y
        # columnas y creando su correspondiente elemento
        for i in range(8):
            for j in range(8):
                elem = self.chess.time_line[-1][i][j]
                if (i+j+2) % 2 == 0:
                    pygame.draw.rect(screen, self.WHITE_COLOR,
                                     (c, r, self.width_block, self.width_block))
                else:
                    pygame.draw.rect(screen, self.GREEN_COLOR,
                                     (c, r, self.width_block, self.width_block))
                if j == self.pos_selected[0] and i == self.pos_selected[1]:
                    pygame.draw.rect(screen,  self.POS_SELECTED_COLOR,
                                     (c, r, self.width_block, self.width_block))
                if elem != '  ':
                    screen.blit(self.icons[elem], (c+4, r+10))

                if self.posPreview[0] == j and self.posPreview[1] == i:
                    screen.blit(self.icons[self.posPreview[2]], (c+4, r+10))
                c += self.width_block
            r += self.width_block
            c = 0

    def run(self):
        environ['SDL_VIDEO_WINDOW_POS'] = '1'  # centrar ventana
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Proyecto 2 - IA - Inversed Chess')
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.running = True

        self.calculateScreen()
        self.pos_selected = [None, None]  # x, y
        on_press = False
        on_revert = False
        on_restart = False
        on_reclamain = False
        bussInfo = []
        reclaimPieceIndex = 0
        self.posPreview = [None, None, None]
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    on_press = False

                if event.type == pygame.KEYUP:
                    on_revert = False
                    on_restart = False

                if on_reclamain and event.type == pygame.MOUSEWHEEL:
                    if (reclaimPieceIndex >= len(self.chess.TO_RECLAIMN)):
                        reclaimPieceIndex = 0
                    self.posPreview[2] = self.chess.TO_RECLAIMN[reclaimPieceIndex]+'1'
                    reclaimPieceIndex += 1

            if len(bussInfo) > 0:
                while len(bussInfo) != 0:
                    info = bussInfo.pop(0)
                    self.infoModal(self.screen, info)
                    pygame.display.flip()
                    sleep(1.1)
            else:
                self.mappingMatrizOnScreen(self.screen)

            current_position = pygame.mouse.get_pos()
            x = int(current_position[0]/self.width_block)
            y = int(current_position[1]/self.width_block)

            if not on_press and pygame.mouse.get_pressed()[0]:
                on_press = True
                last_move = self.chess.time_line[-1]

                # seleciona el destino de la ficha
                if (self.pos_selected[0] is not None and self.pos_selected[1] is not None):

                    if last_move[y][x][1] == '1' and last_move[y][x] != '  ':
                        self.pos_selected[0], self.pos_selected[1] = x, y
                    else:
                        on_reclamain = False
                        pieceToReclaimn = None
                        if self.posPreview[2] is not None:
                            pieceToReclaimn = self.posPreview[2][0]

                        self.posPreview = [None, None, None]

                        if self.pos_selected != [x, y] and threading.active_count() == 1:
                            threading.Thread(name='game-chess', target=self.chess.run, args=(
                                self.pos_selected[0], self.pos_selected[1], x, y, pieceToReclaimn, lambda text: bussInfo.append(text))).start()
                            self.pos_selected[0], self.pos_selected[1] = None, None
                else:  # seleciona la piece
                    if last_move[y][x] != '  ':
                        self.pos_selected[0] = x
                        self.pos_selected[1] = y

                        if (not on_reclamain and last_move[self.pos_selected[1]][self.pos_selected[0]][0] == 'P' and (y+1 == 7)):
                            on_reclamain = True
                            reclaimPieceIndex = 0
                            self.posPreview = [
                                x, y+1, self.chess.TO_RECLAIMN[reclaimPieceIndex]+'1']

            if not on_revert and pygame.key.get_pressed()[pygame.K_a]:
                on_revert = True
                self.chess.revert()

            if not on_restart and pygame.key.get_pressed()[pygame.K_r]:
                on_restart = True
                threading.Thread(target=self.chess.restart).start()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    gui = GUI(WIDTH, HEIGHT)
