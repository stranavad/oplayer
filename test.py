import os

for x in os.listdir('.'):
    if os.path.isfile(x): print('f-' + x)
    elif os.path.isdir(x): print('d-' + x)
    elif os.path.islink(x): print('l-' + x)
    else: print('---' + x)