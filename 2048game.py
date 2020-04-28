from random import randint, choice


class PlayingBoard:
    def __init__(self):
        self._grid = [[0] * 4 for _ in range(4)]
        for _ in range(4):
            self._add_random()

    def __str__(self):
        numbers = []
        for row in self._grid:
            row_nums = []
            for num in row:
                row_nums.append(str(num))
            numbers.append(' '.join(row_nums))
        return '\n'.join(numbers)

    @staticmethod
    def _fill_left(orig: list):
        """Moves all numbers to their left if there is an empty space."""
        new_grid = []
        for row in orig:
            new_row = [n for n in row if n != 0]
            new_row += [0] * (4 - len(new_row))
            new_grid.append(new_row)
        return new_grid

    @staticmethod
    def _move_left(orig: list):
        """Moves the grid left, merging numbers when applicable."""
        board = PlayingBoard._fill_left(orig)
        for row in board:
            for i in range(len(row) - 1):
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    row[i + 1] = 0
        return PlayingBoard._fill_left(board)

    @staticmethod
    def _rotate_grid(grid: list, degree: int):
        """Returns a rotated grid by <degree> degrees clockwise"""
        if degree == 90:
            return [list(row) for row in zip(*grid[::-1])]
        elif degree == -90:
            return [list(row) for row in zip(*grid)][::-1]
        elif degree == 180 or degree == -180:
            return [row[::-1] for row in grid][::-1]

    def _add_random(self):
        if any(0 in row for row in self._grid):
            row = randint(0, 3)
            col = randint(0, 3)
            while self._grid[row][col] != 0:
                row = randint(0, 3)
                col = randint(0, 3)
            addition = choice([2, 4])
            self._grid[row][col] = addition

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
    game = PlayingBoard()
    playing = True
    print(game)

    while playing:
        movement = input()
        game.move(movement)
        print(game)
