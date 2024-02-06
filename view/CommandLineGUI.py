"""
The command line GUI for Jellyblocker
"""

from threading import Thread
from time import sleep
from pynput.keyboard import Listener, KeyCode
import random

from GUI import GUI
from controller.JellyBlocker import JellyBlocker
from model.Jelly import Jelly

class CommandLineGUI(GUI):

    def __init__(self, 
                 jelly_blocker=JellyBlocker()
                 ):
        
        super().__init__(jelly_blocker)

    def update_display(self):
        """
        Print the board to the console and all other info for the user, skipping the top row.
        """

        GUI_lines = [
            "Time: " + str(self.jelly_blocker.game_time // 100) + "." + str(self.jelly_blocker.game_time % 100),
            "Points: " + str(self.jelly_blocker.points),
            "Level: " + str(self.jelly_blocker.level),
            "",
            "Next: "
        ]

        num_jellies_per_line = len(self.jelly_blocker.board.next_falling_group) // 2
        count = 0
        line = ""
        for jelly in self.jelly_blocker.board.next_falling_group:
            line += jelly.color.value
            if count % num_jellies_per_line == 0:
                GUI_lines.append(line)
                line = ""
            count += 1
        GUI_lines.append("")

        for row in self.jelly_blocker.board.board[1:]:
            for jelly in row:
                print(jelly.color.value, end="")
            if len(GUI_lines) > 0:
                line = GUI_lines.pop(0)
                print(" " + line, end="")
            print()
        print()

    def print_controls(self):
        """
        Print every game action and their current keybinds.
        """

        print()
        for binding in self.game_action_key_bindings.keys():
            try:
                print(binding[0].upper() + binding[1:], "-", "[" + self.game_action_key_bindings[binding].char + "]")
            except AttributeError:
                print(binding[0].upper() + binding[1:], "-", "[" + self.game_action_key_bindings[binding].name + "]")

    def print_program_commands(self):
        """
        Print every program action and their current keybinds.
        """

        print()
        for binding in self.program_key_bindings.keys():
            try:
                print(binding[0].upper() + binding[1:], "-", "[" + self.program_key_bindings[binding].char + "]")
            except AttributeError:
                print(binding[0].upper() + binding[1:], "-", "[" + self.program_key_bindings[binding].name + "]")

    def game_over(self):
        print("Game Over! You scored", self.jelly_blocker.points, " points.")
        sleep(1)
        self.print_controls()

    def on_press(self, keybind: KeyCode):
        """
        When the user presses a key, add it to `pressed_keys` and execute the actions of all pressed keys.

        Parameters
        ----------
        keybind : KeyCode
            The key the user pressed.

        Returns
        -------
        bool
            When the user presses the `leave_program` key, return False. Else, return True.
        """

        # add the key to the pressed keys list
        self.pressed_keys.add(keybind)

        # key behavior while game is running
        for pressed_key in self.pressed_keys:
            if self.jelly_blocker.game_running:

                if pressed_key == self.game_action_key_bindings['move left']:
                    self.jelly_blocker.board.move_falling_group_left()
                    self.update_display()
                elif pressed_key == self.game_action_key_bindings['move right']:
                    self.jelly_blocker.board.move_falling_group_right()
                    self.update_display()
                elif pressed_key == self.game_action_key_bindings['rotate left']:
                    self.jelly_blocker.board.rotate_falling_group_left()
                    self.update_display()
                elif pressed_key == self.game_action_key_bindings['rotate right']:
                    self.jelly_blocker.board.rotate_falling_group_right()
                    self.update_display()
                elif pressed_key == self.game_action_key_bindings['fast drop']:
                    self.jelly_blocker.fast_drop = True
            
            # key behavior regardless of whether the game is running or not
            if pressed_key == self.program_key_bindings['leave program']:
                return False
            
            # key behavior if the game is not running
            if not self.jelly_blocker.game_running:
                if pressed_key == self.program_key_bindings['start game']:
                    self.jelly_blocker.game_running = True

                    # create a new thread to run the game and start it
                    run_game_thread = Thread(target=self.jelly_blocker.run_game, args=(self.update_display, self.game_over))
                    run_game_thread.daemon = True
                    run_game_thread.start()
                elif pressed_key == self.program_key_bindings["view controls"]:
                    self.print_controls()

        return True

    def on_release(self, keybind: KeyCode):
        """
        When a key is released, remove it from `pressed_keys` and perform any game actions related to releasing keys.

        Parameters
        ----------
        keybind : KeyCode
            The key the user released.

        Returns
        -------
        bool
            True
        """

        # try removing the key from the pressed_keys list, and return if it wasn't there in the first place
        try:
            self.pressed_keys.remove(keybind)
        except KeyError:
            return True

        # key behavior while game is running
        if self.jelly_blocker.game_running:

            if keybind == self.game_action_key_bindings['fast drop']:
                self.jelly_blocker.fast_drop = False
        
        return True

    def collect_inputs(self):
        """
        Continuously listen for keyboard inputs from the user.
        """

        # collect keyboard inputs indefinitely
        with Listener(
            on_press=self.on_press,
            on_release=self.on_release
            ) as listener:
            listener.join()

    def run_program(self):
        """
        Run to run the command line GUI program for Jelly Blocker.
        """

        # loop until the program is no longer running
        title_jellies = random.sample([Jelly.RED, Jelly.GREEN, Jelly.BLUE, Jelly.PURPLE, Jelly.YELLOW], 4)
        print(title_jellies[0].value + title_jellies[1].value + " Welcome to JellyBlocker " + title_jellies[2].value + title_jellies[3].value)
        self.print_program_commands()
        self.collect_inputs()

        exit(0)

cmd_gui = CommandLineGUI()
cmd_gui.run_program()