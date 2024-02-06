import sys
from pynput.keyboard import Key, Listener, KeyCode

from JellyBlocker import JellyBlocker

class GUI:
    """
    GUI Abstract Class, not to be instantiated
    """

    def __init__(self, 
                 jelly_blocker=JellyBlocker()
                 ):
        
        self.jelly_blocker = jelly_blocker

        self.game_action_key_bindings = {
            'move left': Key.left,
            'move right' : Key.right,
            'rotate left' : KeyCode.from_char('z'),
            'rotate right' : KeyCode.from_char('x'),
            'fast drop' : Key.down,
        }

        self.program_key_bindings = {
            'leave program' : Key.esc,
            'start game' : Key.enter,
            'view controls' : KeyCode.from_char('1')
        }

        self.pressed_keys = set()

    def update_display(self):
        """
        Abstract method for updating the display to be in line with the `self.jelly_blocker` instance.
        """

        pass

    def game_over(self):
        """
        Abstract method for updating the display when the game ends in the `self.jelly_blocker` instance.
        """

        pass