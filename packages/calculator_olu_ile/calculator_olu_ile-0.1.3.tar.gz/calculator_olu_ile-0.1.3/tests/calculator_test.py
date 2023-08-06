
import math
from calculator_olu_ile.calculator import Calculator

cal = Calculator()


def test_add_default_accum_state_path():
    cal.reset()
    cal.add(2)
    assert cal.accum_state == 2, "Should be 2"


def test_add_addition_path():
    cal.reset()
    cal.add(2)
    cal.add(2)
    assert cal.accum_state == 4, "Should be 4"


def test_subtract_default_accum_state_path():
    cal.reset()
    cal.subtract(2)
    assert cal.accum_state == 2, "Should be 2"


def test_subtract_subtraction_path():
    cal.reset()
    cal.subtract(2)
    cal.subtract(2)
    assert cal.accum_state == 0, "Should be 0"


def test_multiply_default_accum_state_path():
    cal.reset()
    cal.multiply(2)
    assert cal.accum_state == 2, "Should be 2"


def test_multiply_multiplication_path():
    cal.reset()
    cal.multiply(2)
    cal.multiply(2)
    assert cal.accum_state == 4, "Should be 4"


def test_divide_default_accum_state_path():
    cal.reset()
    cal.divide(2)
    assert cal.accum_state == 2, "Should be 2"


def test_divide_division_path():
    cal.reset()
    cal.divide(2)
    cal.divide(2)
    assert cal.accum_state == 1, "Should be 1"


def test_root():
    cal.reset()
    cal.root(4)
    assert cal.accum_state == 2, "Should be 2"


def test_reset():
    cal.reset()
    assert cal.accum_state == math.inf, "Should be math.inf or +infinity"
