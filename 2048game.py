from random import choice


class PlayingBoard:
    """
    A class that represents a 2048 game, with the necessary methods
    to manipulate the game state.
    """

    def __init__(self, n: int = 4) -> None:
        """
        Initializes the grid to empty, and adds <n> numbers
        to start off the game.
        """
        self._size = n
        self._grid = [[0] * n for _ in range(n)]
        for _ in range(n):
            self._add_random()

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
        return self._slide_left(self._grid)

    def _move_right(self) -> list:
        """Returns the grid after a right move."""
        rotated = self._rotate_grid(self._grid, 180)
        rotated = self._slide_left(rotated)
        return self._rotate_grid(rotated, -180)

    def _move_up(self) -> list:
        """Returns the grid after a up move."""
        rotated = self._rotate_grid(self._grid, -90)
        rotated = self._slide_left(rotated)
        return self._rotate_grid(rotated, 90)

    def _move_down(self) -> list:
        """Returns the grid after a down move."""
        rotated = self._rotate_grid(self._grid, 90)
        rotated = self._slide_left(rotated)
        return self._rotate_grid(rotated, -90)

    def move(self, direction: str) -> None:
        """
        Responsible for actually modifying the grid using the _move helpers.
        """
        moved = True
        if direction in ['1', 'up', 'u']:
            self._grid = self._move_up()
        elif direction in ['2', 'down', 'd']:
            self._grid = self._move_down()
        elif direction in ['3', 'left', 'l']:
            self._grid = self._move_left()
        elif direction in ['4', 'right', 'r']:
            self._grid = self._move_right()
        else:
            print('invalid direction')
            moved = False
        if moved:
            self._add_random()


if __name__ == '__main__':
    game = PlayingBoard()
    playing = True
    print(game)

    while playing:
        movement = input()
        game.move(movement)
        print(game)
