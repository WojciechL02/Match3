import pygame
from main_menu import MainMenu


if __name__ == "__main__":
    pygame.init()
    width = 800
    height = 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Bejeweled Classic")
    mainMenu = MainMenu(win, width, height)
    mainMenu.run()
