import sys

## change this root dir appropriately
my_math_path = ''

if __name__ == '__main__':
    if not my_math_path in sys.path:
        sys.path.append(my_math_path)

## import py_end_game
from JoustL import *





