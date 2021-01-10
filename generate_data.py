import getopt
import sys

import numpy as np


def get_results(num_rows: int = 10, num_cols: int = 10, file_name: str = None) -> np.ndarray:
    """
    :param      num_rows: int representing number of rows (ie. number of y values or number of rocks left)
    :param      num_cols: int representing number of columns (ie. number of x values or number of rocks picked last)
    :param      file_name: (optional) if passed, will output results to file
    :return:    np.ndarray of ints with shape (num_rows + 1, num_cols).
                1 indicates position is winning
                0 indicates position is losing
                x values begin at 1
                y values begin at 0
    """
    results = np.zeros((num_rows + 1, num_cols), dtype=int)

    def is_position_valid_and_winning(pos_x: int, posy: int):
        """
        :param pos_x: x position after taking x stones
        :param posy: y position after taking x stones
        :return: Boolean representing if move lands at a valid and winning position
        """
        is_x_in_range = pos_x in range(1, num_cols + 1)
        is_y_in_range = posy in range(num_rows + 1)
        return is_x_in_range and is_y_in_range and not results[posy][pos_x - 1]

    for y in range(num_rows + 1):
        for x_base_0 in range(num_cols):
            x = x_base_0 + 1  # Add 1 to x value since indexing is zero based, but we start at x=1

            # Check all 3 possible moves
            take_x_minus_1 = (x - 1, y - (x - 1))
            take_x = (x, y - x)
            take_x_plus_1 = (x + 1, y - (x + 1))
            for x1, y1 in [take_x_minus_1, take_x, take_x_plus_1]:
                if is_position_valid_and_winning(x1, y1):
                    # If possible move lands in valid and losing position, current position is winning
                    results[y][x_base_0] = 1
                    continue
    if file_name:
        np.savetxt(file_name, results[::-1], delimiter=',', newline='\n', fmt='%i')
    return results

def parse():
    options, arguments = getopt.getopt(
        sys.argv[1:],
        'rc:',
        ["num_rows", "num_cols"])
    separator = "\n"
    for o, a in options:
        if o in ("-r", "--num_rows"):
            print(VERSION)
            sys.exit()
        if o in ("-h", "--help"):
            print(USAGE)
            sys.exit()
        if o in ("-s", "--separator"):
            separator = a
    if not arguments or len(arguments) > 3:
        raise SystemExit(USAGE)
    try:
        operands = [int(arg) for arg in arguments]
    except ValueError:
        raise SystemExit(USAGE)
    return separator, operands


if __name__ == "__main__":
    get_results(10000, 200, 'test_data.csv')
