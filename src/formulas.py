"""formulas.py"""


def estimate_reduction_expected_value(y: int, n: int, t: int) -> float:
    epsilon_y = 1e-10
    epsilon_t = 1e-7

    N = y + n + t
    return (y + n) / 2 - (y - n) ** 2 / (2 * N) + y * epsilon_y - t * epsilon_t
