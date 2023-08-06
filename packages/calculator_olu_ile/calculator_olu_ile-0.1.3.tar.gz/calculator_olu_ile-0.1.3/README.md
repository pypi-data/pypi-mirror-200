# Calculator

> Arithmetic calculator with operations add, subtract, divide, multipy and root.


## Installation
```sh
pip install calculator_olu_ile
```

## Usage
```python

For example: Addition with package on IDLE 
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> cal.add(2)
    >>> print(cal.accum_state)
    2
    >>> cal.add(2)
    >>> print(cal.accum_state)
    4

For example: Subtraction with package on IDLE
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> cal.subtract(2)
    >>> print(cal.accum_state)
    2
    >>> cal.subtract(2)
    >>> print(cal.accum_state)
    0

For example: Multiplication with package on IDLE
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> cal.add(2)
    >>> print(cal.accum_state)
    2
    >>> cal.add(2)
    >>> print(cal.accum_state)
    4

For example: Divide with package on IDLE
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> cal.divide(2)
    >>> print(cal.accum_state)
    2
    >>> cal.divide(2)
    >>> print(cal.accum_state)
    1.0

For example: Root with package on IDLE
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> cal.root(4)
    >>> print(cal.accum_state)
    2.0

For example: Reset with package on IDLE
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> cal.reset(2)
    >>> print(cal.accum_state)
    2
```