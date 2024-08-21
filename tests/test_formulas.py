"""test_formulas.py"""

import pytest
from formulas import estimate_reduction_expected_value


def test_estimate_reduction_expected_value():
    # Test case 1
    y, n, t = 10, 5, 15
    expected = (10 + 5) / 2 - (10 - 5) ** 2 / (2 * (10 + 5 + 15)) + 10 * 1e-10
    assert estimate_reduction_expected_value(y, n, t) == pytest.approx(
        expected
    ), "Test case 1 failed"

    # Test case 2
    y, n, t = 20, 10, 30
    expected = (20 + 10) / 2 - (20 - 10) ** 2 / (2 * (20 + 10 + 30)) + 20 * 1e-10
    assert estimate_reduction_expected_value(y, n, t) == pytest.approx(
        expected
    ), "Test case 2 failed"

    # Test case 3
    y, n, t = 5, 2, 8
    expected = (5 + 2) / 2 - (5 - 2) ** 2 / (2 * (5 + 2 + 8)) + 5 * 1e-10
    assert estimate_reduction_expected_value(y, n, t) == pytest.approx(
        expected
    ), "Test case 3 failed"

    # Test case 4
    y, n, t = -10, -5, -15
    expected = (-10 + -5) / 2 - (-10 - -5) ** 2 / (2 * (-10 + -5 + -15)) + -10 * 1e-10
    assert estimate_reduction_expected_value(y, n, t) == pytest.approx(
        expected
    ), "Test case 4 failed"

    # Basic case test
    assert (
        pytest.approx(estimate_reduction_expected_value(10, 5, 2), 0.001) == 6.7647
    ), "Basic case failed"

    # Large number test
    assert (
        pytest.approx(estimate_reduction_expected_value(1000, 500, 200), 0.001)
        == 676.4705
    ), "Large number case failed"

    # Other cases test
    assert (
        pytest.approx(estimate_reduction_expected_value(2, 2, 0), 0.001) == 2.0
    ), "Case y=2, n=2, t=0 failed"
    assert (
        pytest.approx(estimate_reduction_expected_value(2, 2, 0), 0.001) == 2.0
    ), "Case y=2, n=2, t=0 failed"
    assert (
        pytest.approx(estimate_reduction_expected_value(1, 3, 0), 0.001) == 1.5
    ), "Case y=1, n=3, t=0 failed"
    assert (
        pytest.approx(estimate_reduction_expected_value(1, 0, 4), 0.001) == 0.4
    ), "Case y=1, n=0, t=4 failed"
    assert (
        pytest.approx(estimate_reduction_expected_value(1, 1, 2), 0.001) == 1.0
    ), "Case y=1, n=1, t=2 failed"
    assert (
        pytest.approx(estimate_reduction_expected_value(1, 2, 1), 0.001) == 11 / 8
    ), "Case y=1, n=2, t=1 failed"
    assert (
        pytest.approx(estimate_reduction_expected_value(2, 1, 1), 0.001) == 1.5 - 1 / 8
    ), "Case y=2, n=1, t=1 failed"
    assert (
        pytest.approx(estimate_reduction_expected_value(2, 0, 2), 0.001) == 1 / 2
    ), "Case y=2, n=0, t=2 failed"

    # Test case 1: Basic case
    y, n, t = 10, 5, 15
    expected = (
        (10 + 5) / 2 - (10 - 5) ** 2 / (2 * (10 + 5 + 15)) + 10 * 1e-10 - 15 * 1e-7
    )
    assert estimate_reduction_expected_value(y, n, t) == pytest.approx(
        expected
    ), "Test case 1 failed"

    # Test case 2: Large values
    y, n, t = 1000, 500, 2000
    expected = (
        (1000 + 500) / 2
        - (1000 - 500) ** 2 / (2 * (1000 + 500 + 2000))
        + 1000 * 1e-10
        - 2000 * 1e-7
    )
    assert estimate_reduction_expected_value(y, n, t) == pytest.approx(
        expected
    ), "Test case 2 failed"

    # Test case 3: Negative values
    y, n, t = -10, -5, -15
    expected = (
        (-10 + -5) / 2
        - (-10 - -5) ** 2 / (2 * (-10 + -5 + -15))
        + -10 * 1e-10
        - 15 * 1e-7
    )
    assert estimate_reduction_expected_value(y, n, t) == pytest.approx(
        expected
    ), "Test case 3 failed"

    # Test case 4: Zero values
    y, n, t = 0, 0, 0
    with pytest.raises(ZeroDivisionError):
        estimate_reduction_expected_value(y, n, t)

    # Test case 5: Boundary values
    y, n, t = 1, 1, 1
    expected = (1 + 1) / 2 - (1 - 1) ** 2 / (2 * (1 + 1 + 1)) + 1 * 1e-10 - 1 * 1e-7
    assert estimate_reduction_expected_value(y, n, t) == pytest.approx(
        expected
    ), "Test case 5 failed"


if __name__ == "__main__":
    pytest.main()
