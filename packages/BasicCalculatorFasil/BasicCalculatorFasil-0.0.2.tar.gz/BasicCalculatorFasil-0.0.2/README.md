![image](BasicCalculator.png)
## Basic calculator to perform arithmetic operations

This module contains a class `Calculator` that performs basic arithmetic operations. The calculator keeps its memory after each operation unless it is reset. 

## Installation:
To install this package use:
``` 
pip install BasicCalculatorFasil
```

## Implementation:
```python
    from BasicCalculatorFasil import Calculator
    calculator = Calcualtor()
```

#### Addition:

```python
    calculator.add(7)
``` 

#### Subtraction:

```python
    calculator.subtract(3)
``` 

#### Multiplication:

```python
    calculator.multiply(3)
``` 

#### Division:

```python
    calculator.divide(2)
``` 

#### $n^{th}$ root:

```python
    calculator.root(2)
``` 
#### Reset 

```python
    calculator.reset()
``` 

#### to get the current memory of the calculator:
```python
    calculator.memory
``` 

#### Example:
```python
from BasicCalculatorFasil import Calculator
calculator = Calculator()
calculator.reset() # this resets the calculator memory to 0.0
calculator.add(2) # this gives 2
calculator.add(2) # this gives 4
calculator.subtract(5) # this gives -1
calculator.divide(5) # this gives -0.2
calculator.reset() # resetting the calculator back to 0.0
calculator.subtract(5) # this gives -5
calculator.root(3) # this gives some complex number
calculator.root(1/3) # this give a number close to -5 (which was supposed to give back -5)
calculator.add(5) # this give a number close to 0.0  (which was supposed to give back 0.0)
```

## Testing

````
python -m pytest test_BasicCalculatorFasil.py
python -m flake8 BasicCalculatorFasil.py
python -m pyflakes BasicCalculatorFasil.py
python -m mypy BasicCalculatorFasil.py
