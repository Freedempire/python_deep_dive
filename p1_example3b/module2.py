print('Running module2.py')

import module1

def hello():
    print('Module2 says hello\nand...')
    module1.hello()
