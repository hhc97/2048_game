class BoardFavorability:
    """
    A class that calculates how 'good' a given board configuration of 2048 is.
    """

    def __init__(self, grid: list) -> None:
        """Makes copies of the grid, so as to not mutate it."""
        self._grid = [row[:] for row in grid]
        self._numbers = [i for row in grid for i in row]

    def _largest_number_in_corner_score(self) -> int:
        """Assign a score for the largest value being in the corner."""
        largest_num = max(self._numbers)
        if self._grid[0][0] == largest_num:
            return largest_num
        return 0

    def _most_number_of_spaces_score(self) -> int:
        """Returns the number of empty spaces in the grid."""
        return self._numbers.count(0)

    def get_grid_score(self) -> int:
        """
        Returns the final evaluation score associated with this particular
        <self._grid> configuration.
        """
        total_score = 0
        total_score += 1 * self._largest_number_in_corner_score()
        total_score += 50 * self._most_number_of_spaces_score()

        return total_score
