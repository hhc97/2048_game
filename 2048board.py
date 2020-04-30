from random import choice
from favorability import BoardFavorability


class PlayingBoard:
    """
    A class that represents a 2048 game, with the necessary methods
    to manipulate the game state.
    """

    def __init__(self, n: int = 4, grid: list = None) -> None:
        """
        Initializes a <n> by <n> grid if it is not provided,
        and adds <n> numbers to start off the game.
        """
        self._size = n
        if not grid:
            self._grid = [[0] * n for _ in range(n)]
            for _ in range(n):
                self._add_random()
        else:
            self._grid = grid

    def __str__(self) -> str:
        """Returns the string representation of the board for easy printing."""
        numbers = []
        for row in self._grid:
            row_nums = []
            for num in row:
                if num != 0:
                    row_nums.append(str(num))
                else:
                    row_nums.append('.')
            numbers.append(' '.join(row_nums))
        return '\n'.join(numbers)

    def _shift_left(self, orig: list) -> list:
        """Sweeps all numbers as far left as they can go."""
        new_grid = []
        for row in orig:
            new_row = [n for n in row if n != 0]
            new_row += [0] * (self._size - len(new_row))
            new_grid.append(new_row)
        return new_grid

    def _slide_left(self, orig: list) -> list:
        """Moves the grid left, merging numbers when applicable."""
        board = self._shift_left(orig)
        for row in board:
            for i in range(len(row) - 1):
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    row[i + 1] = 0
        return self._shift_left(board)

    @staticmethod
    def _rotate_grid(grid: list, degree: int) -> list:
        """Returns a rotated grid by <degree> degrees clockwise."""
        if degree == 90:
            return [list(row) for row in zip(*grid[::-1])]
        elif degree == -90:
            return [list(row) for row in zip(*grid)][::-1]
        elif degree == 180 or degree == -180:
            return [row[::-1] for row in grid][::-1]

    def _add_random(self) -> bool:
        """
        Checks if there is an empty space to add a new number,
        returns True and modifies the board if there is, and False otherwise.
        """
        if any(0 in row for row in self._grid):
            zero_positions = [[i, j]
                              for i in range(self._size)
                              for j in range(self._size)
                              if self._grid[i][j] == 0]
            row, col = choice(zero_positions)
            to_add = choice([2, 4])
            self._grid[row][col] = to_add
            return True
        return False

    def _move_left(self) -> list:
        """Returns the grid after a left move."""
        final = self._slide_left(self._grid)
        return final if final != self._grid else None

    def _move_right(self) -> list:
        """Returns the grid after a right move."""
        rotated = self._rotate_grid(self._grid, 180)
        rotated = self._slide_left(rotated)
        final = self._rotate_grid(rotated, -180)
        return final if final != self._grid else None

    def _move_up(self) -> list:
        """Returns the grid after a up move."""
        rotated = self._rotate_grid(self._grid, -90)
        rotated = self._slide_left(rotated)
        final = self._rotate_grid(rotated, 90)
        return final if final != self._grid else None

    def _move_down(self) -> list:
        """Returns the grid after a down move."""
        rotated = self._rotate_grid(self._grid, 90)
        rotated = self._slide_left(rotated)
        final = self._rotate_grid(rotated, -90)
        return final if final != self._grid else None

    def _check_game_over(self) -> bool:
        """
        Checks if the game is over by checking if any move is possible.
        Return True if no further move is possible.
        """
        left = self._move_left()
        right = self._move_right()
        up = self._move_up()
        down = self._move_down()
        return not (left or right or up or down)

    def move(self, direction: str) -> bool:
        """
        Responsible for actually modifying the grid using the _move helpers.
        Returns False if there are no further possible moves, True otherwise.
        """
        new_grid = None
        if direction in ['1', 'up', 'u']:
            new_grid = self._move_up()
        elif direction in ['2', 'down', 'd']:
            new_grid = self._move_down()
        elif direction in ['3', 'left', 'l']:
            new_grid = self._move_left()
        elif direction in ['4', 'right', 'r']:
            new_grid = self._move_right()
        else:
            print('invalid move')
        if new_grid:
            self._grid = new_grid
            self._add_random()
            return True
        return not self._check_game_over()

    def _get_favorability(self) -> int:
        """Returns the favorability score of the current grid."""
        return BoardFavorability(self._grid).get_grid_score()

    def smart_move(self, depth: int = 3, first_call=True):
        """Uses BFS to return a suggested move for the current grid state."""
        current_score = self._get_favorability()
        if depth == 0:
            return current_score

        def _score_helper(func):
            moved = func()
            score = -1
            if moved:
                score = PlayingBoard(self._size, moved) \
                    .smart_move(depth - 1, False)
                if current_score > score and not first_call:
                    score = current_score
            return score

        up = _score_helper(self._move_up)
        down = _score_helper(self._move_down)
        left = _score_helper(self._move_left)
        right = _score_helper(self._move_right)

        best = max(up, down, left, right)
        if first_call:
            moves = {up: '1', down: '2', left: '3', right: '4'}
            return moves[best]
        else:
            return best


if __name__ == '__main__':
    game = PlayingBoard()
    playing = True
    print(game)
    move_map = {'1': 'up', '2': 'down', '3': 'left', '4': 'right'}

    while playing:
        move = game.smart_move()
        print(move_map[move], '\n')
        # movement = input()
        if not game.move(move):
            playing = False
        print(game)
    print('game over')
