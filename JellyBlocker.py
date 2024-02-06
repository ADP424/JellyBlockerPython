from time import sleep

from Board import Board
            
class JellyBlocker:
    """
    Controls user input, starting, and stopping the program.

    Attributes
    ----------
    board : Board, default: Board()
        The board the game will be played on.

    num_landed_iterations_before_placement : int, default: 5
        The number of cycles a falling jelly group can stay on the ground before it is placed.

    gravity_speed : int, default: 20
        The time interval between falls for jellies affected by gravity in hundredths of seconds.
    
    num_pops_to_level : int, default: 50
        The number of jellies to pop before leveling up the difficulty.

    falling_speed : int, default: 100
        Time interval between falls for a group of controlled jellies in hundredths of seconds.

    fast_drop_multiplier : int, default: 5
        How much the falling speed should be multiplied when fast drop is active.
    """

    def __init__(self, 
                 board=Board(),
                 num_landed_iterations_before_placement=5,
                 gravity_speed=20,
                 num_pops_to_level=50,
                 falling_speed=100,
                 fast_drop_multiplier=5
                 ):
        self.board = board
        self.num_landed_iterations_before_placement = num_landed_iterations_before_placement
        self.gravity_speed = gravity_speed
        self.num_pops_to_level = num_pops_to_level
        self.falling_speed = falling_speed
        self.fast_drop_multiplier = fast_drop_multiplier

        self.game_running = False
        self.game_time = 0
        self.points = 0
        self.jellies_popped_stat = 0
        self.level = 1
        self.fast_drop = False

    def set_board(self, board: Board):
        """
        Sets the board to a new board.

        Parameters
        ----------
        board : Board
            The new board to replace the old board with.
        """

        self.board = board

    def get_falling_speed(self):
        """
        Calculates and returns falling speed based on `self.level` and `self.fast_drop_multiplier`.

        Returns
        -------
        int
            The calculated falling speed.
        """

        if self.fast_drop:
            return self.falling_speed // self.level // self.fast_drop_multiplier
        return self.falling_speed // self.level

    def run_game(self, update_display, game_over):
        """
        Runs the game until the user hits the game finishes

        Parameters
        ----------
        update_display : function
            The function from the GUI to update the display whenever something on the board changes.

        game_over : function
            The function from the GUI to execute when the game is over.
        """

        # create a new board
        self.set_board(Board())

        # add the first falling group to the board
        self.board.add_falling_group_to_board()

        # loop until the game is over
        count_iterations_without_change = 0
        count_iterations_without_moving_down = 0
        prev_row = 0
        prev_col = 0

        while self.game_running:

            if self.game_time % self.get_falling_speed() == 0:
                
                # move the falling group down
                # if the falling group didn't move down, tick the counter up
                if not self.board.move_falling_group_down():
                    count_iterations_without_moving_down += 1
                else:
                    count_iterations_without_moving_down = 0

                # if the falling group hasn't moved since last iteration, tick the counter up
                if prev_row == self.board.current_falling_group[0].row and prev_col == self.board.current_falling_group[0].col:
                    count_iterations_without_change += 1
                else:
                    count_iterations_without_change = 0

                # if the falling group hasn't been moved for `num_landed_iterations_before_placement // 2` iterations, place it
                # if the falling group hasn't moved down in `num_landed_iterations_before_placement` iterations, place it
                if count_iterations_without_change >= self.num_landed_iterations_before_placement // 2 or \
                   count_iterations_without_moving_down >= self.num_landed_iterations_before_placement:
                    
                    # place the current falling group, get a new one, and pop jellies
                    if not self.board.cycle_falling_groups():
                        self.game_running = False
                        game_over()
                        return

                    total_jellies_popped = 0
                    popping_chain = -1

                    # emulating do-while loop, look at the break condition at the bottom of the loop
                    while True:

                        # apply gravity until all jellies are on the ground
                        board_changed = True
                        while board_changed:
                            update_display()
                            board_changed = self.board.apply_gravity()
                            sleep(self.gravity_speed / 100)

                        # pop any jellies that are now in large enough groups
                        num_jellies_popped = self.board.pop_jellies()
                        total_jellies_popped += num_jellies_popped
                        self.jellies_popped_stat += num_jellies_popped
                        popping_chain += 2

                        if num_jellies_popped == 0:
                            break
                        num_jellies_popped = 0

                        # if enough jellies have been popped to level up, level up
                        if self.jellies_popped_stat >= self.num_pops_to_level * self.level:
                            self.level += 1
                    
                        # this is how points are calculated, given to the user after every pop in a chain
                        self.points += total_jellies_popped * popping_chain

                    count_iterations_without_change = 0
                    count_iterations_without_moving_down = 0

                prev_row = self.board.current_falling_group[0].row
                prev_col = self.board.current_falling_group[0].col
                update_display()

            sleep(0.01)
            self.game_time += 1