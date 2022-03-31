import pygame
import time
import copy
from os import path
from board_model import Board


class HighScoreFileError(FileNotFoundError):
    pass


class AudioFileError(FileNotFoundError):
    pass


class GraphicFileError(FileNotFoundError):
    pass


class Game:
    def __init__(self, window: object, board_size: int):
        """
        Creates instance of game.
        """
        # GAME VARIABLES
        self._window = window
        self._cell_size = 40
        self._board_size = board_size
        self._level = 1
        self._level_score_limit = 50
        self._score = 0
        self._font = pygame.font.SysFont('BROADWAY', 30)
        self._big_font = pygame.font.SysFont('BROADWAY', 60)
        self._read_high_score_from_file()
        # MUSIC
        self._load_music()
        # GRAPHICS
        self._load_graphics()

    def _read_high_score_from_file(self):
        try:
            with open('high_score.txt', 'r') as file:
                text = file.readline()
                if text.isdigit():
                    self.set_high_score(int(text))
                else:
                    self.set_high_score(0)
        except FileNotFoundError as e:
            raise HighScoreFileError from e

    def _load_music(self):
        file_existence_table = [
            path.isfile('audio/music.mp3'),
            path.isfile('audio/3_match.wav'),
            path.isfile('audio/4_match.wav'),
            path.isfile('audio/5_match.wav'),
            path.isfile('audio/go.mp3'),
            path.isfile('audio/level_complete.mp3'),
            path.isfile('audio/game_over.mp3'),
            path.isfile('audio/high_score.wav')
        ]
        if all(file_existence_table):
            self._music = pygame.mixer.music.load('audio/music.mp3')
            self._match3_sound = pygame.mixer.Sound('audio/3_match.wav')
            self._match4_sound = pygame.mixer.Sound('audio/4_match.wav')
            self._match5_sound = pygame.mixer.Sound('audio/5_match.wav')
            self._go_sound = pygame.mixer.Sound('audio/go.mp3')
            self._level_complete_sound = pygame.mixer.Sound('audio/level_complete.mp3') # noqa
            self._game_over_sound = pygame.mixer.Sound('audio/game_over.mp3')
            self._new_high_score_sound = pygame.mixer.Sound('audio/high_score.wav') # noqa
        else:
            raise AudioFileError

    def _load_graphics(self):
        file_existence_table = [
            path.isfile('assets/selection.png'),
            path.isfile('assets/background.png'),
            path.isfile('assets/red.png'),
            path.isfile('assets/blue.png'),
            path.isfile('assets/green.png'),
            path.isfile('assets/orange.png'),
            path.isfile('assets/pink.png'),
            path.isfile('assets/white.png'),
            path.isfile('assets/yellow.png')
        ]
        if all(file_existence_table):
            self._selection = pygame.image.load('assets/selection.png')
            self._bg = pygame.image.load('assets/background.png')
            self._jewels = {
                1: pygame.image.load('assets/red.png'),
                2: pygame.image.load('assets/blue.png'),
                3: pygame.image.load('assets/green.png'),
                4: pygame.image.load('assets/orange.png'),
                5: pygame.image.load('assets/pink.png'),
                6: pygame.image.load('assets/white.png'),
                7: pygame.image.load('assets/yellow.png')
            }
        else:
            raise GraphicFileError

    def get_window(self) -> object:
        return self._window

    def get_cell_size(self) -> int:
        return self._cell_size

    def get_board_size(self) -> int:
        return self._board_size

    def get_level(self) -> int:
        return self._level

    def get_level_score_limit(self) -> int:
        return self._level_score_limit

    def next_level_score_limit(self):
        self._level_score_limit *= 2

    def get_score(self) -> int:
        return self._score

    def add_score(self, points: int):
        self._score += points

    def get_jewel_color(self, color: int) -> object:
        return self._jewels[color]

    def get_music(self) -> object:
        return self._music

    def get_match3_sound(self) -> object:
        return self._match3_sound

    def get_match4_sound(self) -> object:
        return self._match4_sound

    def get_match5_sound(self) -> object:
        return self._match5_sound

    def get_go_sound(self) -> object:
        return self._go_sound

    def get_level_complete_sound(self) -> object:
        return self._level_complete_sound

    def get_game_over_sound(self) -> object:
        return self._game_over_sound

    def get_new_high_score_sound(self) -> object:
        return self._new_high_score_sound

    def get_high_score(self) -> int:
        return self._high_score

    def set_high_score(self, score: int):
        self._high_score = score

    def get_font(self):
        return self._font

    def get_big_font(self):
        return self._big_font

    def get_selection(self) -> object:
        return self._selection

    def get_bg(self) -> object:
        return self._bg

    def save_score_to_file(self):
        with open('high_score.txt', 'w') as file:
            file.write(f'{self.get_high_score()}')

    def set_music_settings(self):
        pygame.mixer_music.set_volume(0.1)
        self.get_match3_sound().set_volume(0.25)
        self.get_match4_sound().set_volume(0.25)
        self.get_match5_sound().set_volume(0.25)
        self.get_go_sound().set_volume(0.3)
        self.get_level_complete_sound().set_volume(0.3)
        self.get_game_over_sound().set_volume(0.3)
        self.get_new_high_score_sound().set_volume(0.3)

    def draw_window(self, grid: list):
        """
        Draws graphics.
        """
        color = (255, 255, 255)
        font = self.get_font()
        # draw background
        self.get_window().blit(self.get_bg(), (0, 0))

        # draw high_score
        high_score = self.get_high_score()
        text_high_score = font.render(f'High score: {high_score}', True, color)
        self.get_window().blit(text_high_score, (10, 50))

        # draw score
        score = font.render(f'Score: {self.get_score()}', True, color)
        self.get_window().blit(score, (10, 90))

        # draw level number
        level = font.render(f'Level {self.get_level()}', True, color)
        self.get_window().blit(level, (10, 10))

        # draw board
        for row in range(self.get_board_size()):
            for column in range(self.get_board_size()):
                cell = grid[row][column]
                jewel_color = self.get_jewel_color(cell.get_color())
                position = (400 + cell.get_x() * self.get_cell_size(),
                            80 + cell.get_y() * self.get_cell_size())
                self.get_window().blit(jewel_color, position)
        pygame.display.update()

    def draw_selection(self, coords: list):
        """
        Draws the selection frame.
        """
        size = self.get_cell_size()
        position = (400 + coords[1] * size, 80 + coords[0] * size)
        self.get_window().blit(self.get_selection(), position)
        pygame.display.update()

    def new_high_score(self):
        """
        Informs about a new record.
        """
        big_font = self.get_big_font()
        text = big_font.render('NEW HIGH SCORE!', True, (255, 255, 255))
        self.get_window().blit(text, (100, 200))
        pygame.display.update()
        self.get_new_high_score_sound().play()

    def next_level(self):
        """
        Informs about next level.
        """
        big_font = self.get_big_font()
        self._level += 1
        text = big_font.render('LEVEL COMPLETE', True, (255, 255, 255))
        self.get_window().blit(text, (100, 200))
        pygame.display.update()
        self.get_level_complete_sound().play()

    def game_over(self):
        """
        Informs about failure.
        """
        text = self.get_big_font().render('GAME OVER!', True, (255, 255, 255))
        self.get_window().blit(text, (210, 220))
        pygame.display.update()
        self.get_game_over_sound().play()
        time.sleep(3)

    def run(self):
        """
        Game logic.
        """
        run = True
        high_scored = False
        pygame.font.init()
        pygame.mixer.music.play(-1)

        self.set_music_settings()

        clicks = 0
        selected = []

        board = Board(self.get_board_size())

        self.draw_window(board.get_grid())

        last_grid = copy.deepcopy(board)
        self.get_go_sound().play()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] in range(400, 721) and pos[1] in range(80, 400):
                        clicks += 1
                        cell_coords = ((pos[1]-80) // 40, (pos[0]-400) // 40)
                        selected.append(cell_coords)
                        if clicks == 1:
                            self.draw_selection(cell_coords)
                        elif clicks == 2:
                            clicks = 0
                            selection_result, match, score = last_grid.handle_selected_jewels(selected) # noqa
                            last_grid.set_grid(selection_result)
                            new_grid = last_grid
                            while match != []:
                                self.add_score(score)
                                self.draw_window(new_grid.get_grid())
                                pygame.display.update()

                                # match sounds
                                if score >= 5:
                                    self.get_match5_sound().play()
                                elif score == 3:
                                    self.get_match3_sound().play()
                                elif score == 4:
                                    self.get_match4_sound().play()

                                time.sleep(1)
                                new_grid.set_grid(new_grid.delete_jewels(match, self.get_level())) # noqa
                                match, score = new_grid.find_cells_to_delete() # noqa
                            last_grid = copy.deepcopy(new_grid)
                            selected = []

                            # obsługa high score
                            if self.get_score() > self.get_high_score():
                                self.set_high_score(self.get_score())
                                if not high_scored:
                                    high_scored = True
                                    self.new_high_score()
                                    time.sleep(1)
                            if self.get_score() >= self.get_level_score_limit(): # noqa
                                self.next_level_score_limit()
                                self.next_level()
                                time.sleep(1)
                                last_grid.set_grid(last_grid.generate_grid(self.get_level())) # noqa
                                self.draw_window(last_grid.get_grid())
                                pygame.display.update()
                                break

                            self.draw_window(last_grid.get_grid())

                        # game over
                        if last_grid.check_lost(last_grid.get_grid()):
                            self.game_over()
                            run = False
                        pygame.display.update()

        # save high score
        if high_scored:
            self.save_score_to_file()
        pygame.mixer.music.stop()
