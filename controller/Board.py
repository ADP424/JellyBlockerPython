import random

from model.Jelly import Jelly, JellyBlock

class Board:
    """
    The board that keeps track of the game state.

    Attributes
    ----------
    width : int, default: 6
        The width of the board.
    
    height : int, default: 13
        The height of the board, with the top row being off-screen.

    num_colors : int, default: 4
        The number of colors to choose from when generating jellies.

    possible_sizes : list, default: [2]
        The possible sizes to choose from when generating jelly falling groups.

    num_connecting_jellies_to_pop : int, default: 4
        The number of connected jellies required to pop.
    """

    def __init__(self, 
                 width=6, 
                 height=13, 
                 num_colors=4, 
                 possible_sizes=[2],
                 num_connecting_jellies_to_pop=4
                 ):
        self.width = width
        self.height = height
        self.num_colors = num_colors
        self.possible_sizes = possible_sizes
        self.num_connecting_jellies_to_pop = num_connecting_jellies_to_pop

        self.board = [[JellyBlock() for _ in range(width)] for _ in range(height)]
        self.colors = random.sample(
            [Jelly.RED, Jelly.GREEN, Jelly.BLUE, Jelly.PURPLE, Jelly.YELLOW],
            num_colors)
        self.current_falling_group = self.get_random_jelly_falling_group()
        self.next_falling_group = self.get_random_jelly_falling_group()

    def get_random_jelly_falling_group(self):
        """
        Create a random jelly falling group based on `self.num_colors` and `self.possible_sizes`.

        Returns
        -------
        list
            The random falling group.
        """

        falling_group = [JellyBlock(falling=True) for _ in range(random.choice(self.possible_sizes))]
        for jelly in falling_group:
            jelly.color = random.choice(self.colors)
        return falling_group
    
    def add_falling_group_to_board(self) -> bool:
        """
        Insert the current falling group in the top of the board, replace it with the next falling group,
        and replace the next falling group with a random falling group.

        Returns
        -------
        bool
            Whether there was space for the falling group.
        
        Notes
        -----
        The falling group list is ordered from left to right, then up to down.
        Ex. A falling group has four jellies with (row, col) coordinates: [(0, 0), (1, 0), (0, 1), (1, 1)].
        """

        row = 0
        col = (self.width - 1) // 2
        for jelly in self.current_falling_group:
            if self.board[row][col].color != Jelly.EMPTY:
                return False
            jelly.row = row
            jelly.col = col
            self.board[row][col] = jelly
            row += 1

            # if the third row is reached, wrap and add to the next col instead
            if row >= 2:
                row = 0
                col += 1

        return True

    def move_falling_group_left(self):
        """
        If there is space for the falling group leftwards, move the falling group left.

        Notes
        -----
        The method scans the falling jellies from first to last in the list, because falling jellies
        are listed in order from left to right.
        """

        is_space_to_move = True
        for jelly in self.current_falling_group:

            # if there is either a blank space or a falling jelly to the left, there is space for this jelly
            if jelly.col == 0 or (self.board[jelly.row][jelly.col - 1].color != Jelly.EMPTY and \
               not self.board[jelly.row][jelly.col - 1].falling):
                is_space_to_move = False
                break
        
        if is_space_to_move:
            for jelly in self.current_falling_group:
                self.board[jelly.row][jelly.col - 1] = jelly
                self.board[jelly.row][jelly.col] = JellyBlock()
                jelly.col -= 1

    def move_falling_group_right(self):
        """
        If there is space for the falling group rightwards, move the falling group right.

        Notes
        -----
        The method scans the falling jellies from last to first in the list, because falling jellies
        are listed in order from left to right.
        """

        is_space_to_move = True
        for jelly in reversed(self.current_falling_group):

            # if there is either a blank space or a falling jelly to the right, there is space for this jelly
            if jelly.col == self.width - 1 or (self.board[jelly.row][jelly.col + 1].color != Jelly.EMPTY and \
                not self.board[jelly.row][jelly.col + 1].falling):
                is_space_to_move = False
                break
        
        if is_space_to_move:
            for jelly in reversed(self.current_falling_group):
                self.board[jelly.row][jelly.col + 1] = jelly
                self.board[jelly.row][jelly.col] = JellyBlock()
                jelly.col += 1

    def rotate_falling_group_left(self):
        """
        If there is space to rotate counterclockwise, rotate the falling group counterclockwise.

        Notes
        -----
        Falling groups of size 1 aren't rotated.
        Falling groups of size 2 rotate by spinning a jelly around another one.
        Falling groups greater than size 2, I haven't figured out yet :/
        """

        if len(self.current_falling_group) == 1:
            return
        
        if len(self.current_falling_group) == 2:
            
            # if the jellies are vertical, move the top one to the left of the bottom
            if self.current_falling_group[0].row != self.current_falling_group[1].row and \
               self.current_falling_group[0].col > 0 and \
               self.board[self.current_falling_group[0].row][self.current_falling_group[0].col - 1].color == Jelly.EMPTY and \
               self.board[self.current_falling_group[0].row + 1][self.current_falling_group[0].col - 1].color == Jelly.EMPTY:

                # move the first jelly
                self.board[self.current_falling_group[0].row + 1][self.current_falling_group[0].col - 1] = self.current_falling_group[0]
                self.board[self.current_falling_group[0].row][self.current_falling_group[0].col] = JellyBlock()
                self.current_falling_group[0].row += 1
                self.current_falling_group[0].col -= 1

            # if the jellies are horizontal, move the right one up and the left one right
            elif self.current_falling_group[0].col != self.current_falling_group[1].col and \
               self.current_falling_group[0].row > 0 and \
               self.board[self.current_falling_group[0].row - 1][self.current_falling_group[0].col].color == Jelly.EMPTY:
                
                # move the second jelly
                self.board[self.current_falling_group[1].row - 1][self.current_falling_group[1].col] = self.current_falling_group[1]
                self.current_falling_group[1].row -= 1

                # move the first jelly
                self.board[self.current_falling_group[0].row][self.current_falling_group[0].col + 1] = self.current_falling_group[0]
                self.board[self.current_falling_group[0].row][self.current_falling_group[0].col] = JellyBlock()
                self.current_falling_group[0].col += 1

                # swap the positions of the jellies in the falling group list to maintain left-right, up-down order
                temp = self.current_falling_group[0]
                self.current_falling_group[0] = self.current_falling_group[1]
                self.current_falling_group[1] = temp
        else:
            # TODO
            pass

    def rotate_falling_group_right(self):
        """
        If there is space to rotate clockwise, rotate the falling group clockwise.

        Notes
        -----
        Falling groups of size 1 aren't rotated.
        Falling groups of size 2 rotate by spinning a jelly around another one.
        Falling groups greater than size 2 rotate by shifting every jelly clockwise.
        """

        if len(self.current_falling_group) == 1:
            return
        
        if len(self.current_falling_group) == 2:
            
            # if the jellies are vertical, move the top one to the right of the bottom
            if self.current_falling_group[0].row != self.current_falling_group[1].row and \
               self.current_falling_group[0].col < self.width - 1 and \
               self.board[self.current_falling_group[0].row][self.current_falling_group[0].col + 1].color == Jelly.EMPTY and \
               self.board[self.current_falling_group[0].row + 1][self.current_falling_group[0].col + 1].color == Jelly.EMPTY:

                # move the first jelly
                self.board[self.current_falling_group[0].row + 1][self.current_falling_group[0].col + 1] = self.current_falling_group[0]
                self.board[self.current_falling_group[0].row][self.current_falling_group[0].col] = JellyBlock()
                self.current_falling_group[0].row += 1
                self.current_falling_group[0].col += 1

                # swap the positions of the jellies in the falling group list to maintain left-right, up-down order
                temp = self.current_falling_group[0]
                self.current_falling_group[0] = self.current_falling_group[1]
                self.current_falling_group[1] = temp

            # if the jellies are horizontal, move the left one up and the right one left
            elif self.current_falling_group[0].col != self.current_falling_group[1].col and \
               self.current_falling_group[0].row > 0 and \
               self.board[self.current_falling_group[0].row - 1][self.current_falling_group[0].col].color == Jelly.EMPTY:
                
                # move the first jelly
                self.board[self.current_falling_group[0].row - 1][self.current_falling_group[0].col] = self.current_falling_group[0]
                self.current_falling_group[0].row -= 1

                # move the second jelly
                self.board[self.current_falling_group[1].row][self.current_falling_group[1].col - 1] = self.current_falling_group[1]
                self.board[self.current_falling_group[1].row][self.current_falling_group[1].col] = JellyBlock()
                self.current_falling_group[1].col -= 1
        else:
            # TODO
            pass

    def move_falling_group_down(self) -> bool:
        """
        Move the falling group down by one, if able.

        Returns
        -------
        bool
            Whether the falling group moved down or not.
        """

        # if there is ground or a non-falling jelly below any of the jellies, it can't move down
        can_move_down = True
        for jelly in reversed(self.current_falling_group):
            if jelly.row == self.height - 1 or (not self.board[jelly.row + 1][jelly.col].falling and \
               self.board[jelly.row + 1][jelly.col].color != Jelly.EMPTY):
                can_move_down = False
        
        if can_move_down:
            for jelly in reversed(self.current_falling_group):
                self.board[jelly.row + 1][jelly.col] = jelly
                self.board[jelly.row][jelly.col] = JellyBlock()
                jelly.row += 1

        return can_move_down
    
    def cycle_falling_groups(self) -> bool:
        """
        Place the current falling group, cycle the next falling group, and replace that next falling group.

        Returns
        -------
        bool
            Whether there was space to place the falling group or not
        """
        
        # place the current falling group
        for jelly in self.current_falling_group:
            jelly.falling = False
        
        # set the current equal to the next, get a new next, and add the next to the board
        self.current_falling_group = self.next_falling_group
        self.next_falling_group = self.get_random_jelly_falling_group()
        return self.add_falling_group_to_board()

    def pop_jellies(self) -> int:
        """
        Iterate through the board to find jellies needing popping and return the number of jellies popped.

        Returns
        -------
        int
            The number of jellies popped.
        """

        num_jellies_popped = 0

        # explore every path from each jelly using pseudo-BFS
        total_visited_jellies = {}
        for row in self.board:
            for jelly in row:

                # if the jelly is empty, garbage, falling, or visited already, continue
                if jelly.color == Jelly.EMPTY or jelly.color == Jelly.GARBAGE or \
                   jelly.falling or total_visited_jellies.get(jelly, False):
                    continue

                jelly_queue = [jelly]
                visited_jellies = [jelly]
                total_visited_jellies[jelly] = True

                while len(jelly_queue) > 0:
                    adj_jelly = jelly_queue.pop(0)

                    # add all adjacent, same-colored, unvisited jellies to the list to visit
                    if adj_jelly.row > 0 and \
                       self.board[adj_jelly.row - 1][adj_jelly.col].color != Jelly.EMPTY and \
                       self.board[adj_jelly.row - 1][adj_jelly.col].color != Jelly.GARBAGE and \
                       not total_visited_jellies.get(self.board[adj_jelly.row - 1][adj_jelly.col], False) and \
                       adj_jelly.color == self.board[adj_jelly.row - 1][adj_jelly.col].color:
                        jelly_queue.append(self.board[adj_jelly.row - 1][adj_jelly.col])
                        visited_jellies.append(self.board[adj_jelly.row - 1][adj_jelly.col])
                        total_visited_jellies[self.board[adj_jelly.row - 1][adj_jelly.col]] = True

                    if adj_jelly.row < self.height - 1 and \
                       self.board[adj_jelly.row + 1][adj_jelly.col].color != Jelly.EMPTY and \
                       self.board[adj_jelly.row + 1][adj_jelly.col].color != Jelly.GARBAGE and \
                       not total_visited_jellies.get(self.board[adj_jelly.row + 1][adj_jelly.col], False) and \
                       adj_jelly.color == self.board[adj_jelly.row + 1][adj_jelly.col].color:
                        jelly_queue.append(self.board[adj_jelly.row + 1][adj_jelly.col])
                        visited_jellies.append(self.board[adj_jelly.row + 1][adj_jelly.col])
                        total_visited_jellies[self.board[adj_jelly.row + 1][adj_jelly.col]] = True

                    if adj_jelly.col > 0 and \
                       self.board[adj_jelly.row][adj_jelly.col - 1].color != Jelly.EMPTY and \
                       self.board[adj_jelly.row][adj_jelly.col - 1].color != Jelly.GARBAGE and \
                       not total_visited_jellies.get(self.board[adj_jelly.row][adj_jelly.col - 1], False) and \
                       adj_jelly.color == self.board[adj_jelly.row][adj_jelly.col - 1].color:
                        jelly_queue.append(self.board[adj_jelly.row][adj_jelly.col - 1])
                        visited_jellies.append(self.board[adj_jelly.row][adj_jelly.col - 1])
                        total_visited_jellies[self.board[adj_jelly.row][adj_jelly.col - 1]] = True

                    if adj_jelly.col < self.width - 1 and \
                       self.board[adj_jelly.row][adj_jelly.col + 1].color != Jelly.EMPTY and \
                       self.board[adj_jelly.row][adj_jelly.col + 1].color != Jelly.GARBAGE and \
                       not total_visited_jellies.get(self.board[adj_jelly.row][adj_jelly.col + 1], False) and \
                       adj_jelly.color == self.board[adj_jelly.row][adj_jelly.col + 1].color:
                        jelly_queue.append(self.board[adj_jelly.row][adj_jelly.col + 1])
                        visited_jellies.append(self.board[adj_jelly.row][adj_jelly.col + 1])
                        total_visited_jellies[self.board[adj_jelly.row][adj_jelly.col + 1]] = True
                    
                # if the number of connected jellies is enough to pop, pop them
                if len(visited_jellies) >= self.num_connecting_jellies_to_pop:
                    num_jellies_popped += len(visited_jellies)
                    for jelly_to_pop in visited_jellies:
                        self.board[jelly_to_pop.row][jelly_to_pop.col] = JellyBlock()

        return num_jellies_popped

    def apply_gravity(self) -> bool:
        """
        Iterate through the board and move every jelly in the air down by 1.

        Returns
        -------
        bool
            Whether any jellies were actually moved downward.
        """

        board_changed = False
        for row in reversed(range(len(self.board) - 1)):
            for col in range(len(self.board[row])):

                # if the jelly isn't falling and isn't on another jelly, move it down by 1
                if self.board[row][col].color != Jelly.EMPTY and not self.board[row][col].falling \
                    and self.board[row + 1][col].color == Jelly.EMPTY:
                    self.board[row + 1][col] = self.board[row][col]
                    self.board[row + 1][col].row += 1
                    self.board[row][col] = JellyBlock()
                    board_changed = True

        return board_changed

    def hard_drop(self):
        """
        Drop the falling group to the ground immediately
        """