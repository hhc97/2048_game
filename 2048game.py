from random import randint, choice


class PlayingBoard:
    def __init__(self, n: int = 4):
        self._size = n
        self._grid = [[0] * n for _ in range(n)]
        for _ in range(n):
            self._add_random()

    def __str__(self):
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

    def _fill_left(self, orig: list):
        """Moves all numbers to their left if there is an empty space."""
        new_grid = []
        for row in orig:
            new_row = [n for n in row if n != 0]
            new_row += [0] * (self._size - len(new_row))
            new_grid.append(new_row)
        return new_grid

    def _move_left(self, orig: list):
        """Moves the grid left, merging numbers when applicable."""
        board = self._fill_left(orig)
        for row in board:
            for i in range(len(row) - 1):
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    row[i + 1] = 0
        return self._fill_left(board)

    @staticmethod
    def _rotate_grid(grid: list, degree: int):
        """Returns a rotated grid by <degree> degrees clockwise"""
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

    def move_left(self):
        self._grid = self._move_left(self._grid)
        self._add_random()

    def move_right(self):
        rotated = self._rotate_grid(self._grid, 180)
        rotated = self._move_left(rotated)
        self._grid = self._rotate_grid(rotated, -180)
        self._add_random()

    def move_up(self):
        rotated = self._rotate_grid(self._grid, -90)
        rotated = self._move_left(rotated)
        self._grid = self._rotate_grid(rotated, 90)
        self._add_random()

    def move_down(self):
        rotated = self._rotate_grid(self._grid, 90)
        rotated = self._move_left(rotated)
        self._grid = self._rotate_grid(rotated, -90)
        self._add_random()

    def move(self, direction: str):
        if direction in ['1', 'up', 'u']:
            self.move_up()
        elif direction in ['2', 'down', 'd']:
            self.move_down()
        elif direction in ['3', 'left', 'l']:
            self.move_left()
        elif direction in ['4', 'right', 'r']:
            self.move_right()
        else:
            print('invalid direction')


if __name__ == '__main__':
    game = PlayingBoard(4)
    playing = True
    print(game)

    while playing:
        movement = input()
        game.move(movement)
        print(game)
