import pygame

from graphics.colors import WHITE


def write_text(screen, txt, x, y, size, color=WHITE, font='freesansbold.ttf'):
    """
    write text on the screen
    :param screen: the screen to write on
    :param txt: text to write
    :param x: middle x of the text position
    :param y: middle y of the text position
    :param size: font size
    :param color: color of the text
    :param font: font of the text
    :return:
    """
    font = pygame.font.Font(font, size)
    # create a text surface object, on which text is drawn on it.
    text = font.render(txt, True, color)
    # create a rectangular object for the text surface object
    textRect = text.get_rect()
    # set the center of the rectangular object.
    textRect.center = (x, y)
    # write the text
    screen.blit(text, textRect)
