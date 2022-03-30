import sys
import time
import pathlib
import os

b = pathlib.Path(__file__).parent.resolve()
print(b)



time.sleep(1)
print(f'The number from route is: {sys.argv[1:][0]}')
print('This is HELLO from python script.')
