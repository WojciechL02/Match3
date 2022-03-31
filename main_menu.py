from game import AudioFileError, Game, GraphicFileError, HighScoreFileError
import pygame
from os import path
from typing import Tuple


class MainMenu:
    def __init__(self, window: object, width: int, height: int) -> None:
        self._window = window
        self._width = width
        self._height = height
        self._board_size = 8
        self._broken_files = False
        # GRAPHICS
        self.load_graphics_from_file()

    def load_graphics_from_file(self):
        file_existence_table = [
            path.isfile('assets/main_menu_bg.jpg'),
            path.isfile('assets/logo.png'),
            path.isfile('assets/start.png')
        ]
        if all(file_existence_table):
            self._bg = pygame.image.load('assets/main_menu_bg.jpg')
            scale = (self.get_width(), self.get_height())
            self._bg = pygame.transform.scale(self.get_bg(), scale)
            self._logo = pygame.image.load('assets/logo.png')
            self._start_button = pygame.image.load('assets/start.png')
            self._button_pos = (
                self.get_width() / 2 - self.get_start_button().get_width() / 2,
                350
            )
        else:
            msg = 'Missing graphic files! ("assets" directory)'
            self.draw_file_error_message(msg)

    def draw_file_error_message(self, text: str):
        self._broken_files = True
        color = (255, 255, 255)
        font = pygame.font.SysFont('BROADWAY', 30)

        self.get_window().fill((0, 0, 0))

        msg1 = font.render(text, True, color)
        msg2 = font.render('Reinstall the game.', True, color)
        self.get_window().blit(msg1, (80, 200))
        self.get_window().blit(msg2, (250, 240))
        pygame.display.update()

        # Wait until the user clicks QUIT
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

    def get_window(self) -> object:
        return self._window

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_bg(self) -> object:
        return self._bg

    def get_logo(self):
        return self._logo

    def get_start_button(self):
        return self._start_button

    def get_button_pos(self) -> Tuple[int, int]:
        return self._button_pos

    def get_board_size(self) -> int:
        return self._board_size

    def run(self):
        if not self._broken_files:
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        left_border = self.get_button_pos()[0]
                        right_border = self.get_button_pos()[0]\
                            + self.get_start_button().get_width()
                        top_border = self.get_button_pos()[1]
                        bottom_border = self.get_button_pos()[1]\
                            + self.get_start_button().get_height()

                        if left_border <= x <= right_border:
                            if top_border <= y <= bottom_border:
                                try:
                                    game = Game(self.get_window(),
                                                self.get_board_size())
                                    game.run()
                                    del game
                                except HighScoreFileError:
                                    run = False
                                    msg = 'Missing "high_score.txt" file!'
                                    self.draw_file_error_message(msg)
                                except AudioFileError:
                                    run = False
                                    msg = 'Missing audio files! ("audio" directory)' # noqa
                                    self.draw_file_error_message(msg)
                                except GraphicFileError:
                                    run = False
                                    msg = 'Missing graphic files! ("assets" directory)' # noqa
                                    self.draw_file_error_message(msg)
                self.draw()
            pygame.quit()

    def draw(self):
        font = pygame.font.SysFont('BROADWAY', 14)
        color = (255, 255, 255)

        # BACKGROUND
        self.get_window().blit(self.get_bg(), (0, 0))

        # ASSETS AUTHOR
        text = 'Assets author: github.com/mmabraham'
        assets_author = font.render(text, True, color)
        self.get_window().blit(assets_author, (10, 480))

        # LOGO
        logo_pos = (self.get_width() / 2 - self.get_logo().get_width() / 2, 0)
        self.get_window().blit(self.get_logo(), logo_pos)

        # START BUTTON
        bttn_pos = (self.get_button_pos()[0], self.get_button_pos()[1])
        self.get_window().blit(self.get_start_button(), bttn_pos)

        pygame.display.update()
