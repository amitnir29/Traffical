from gui.gui_flow import gui_manager
from gui.screen import create_screen, quit_screen


def main():
    # size of window
    win_width, win_height = (800, 800)
    screen = create_screen(win_width, win_height)
    # run the menu
    gui_manager.run(screen)
    # quit at the end
    quit_screen()


if __name__ == '__main__':
    main()
