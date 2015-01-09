__author__ = 'Tecnoman5000'
import time


for i in range(101):                        # for 0 to 100
    s = str(i) + '%'                        # string for output
    print(s, end='')                        # just print and flush
    print('\r' * len(s), end='')                 # use '\r' to go back
    time.sleep(0.2)                         # sleep for 200ms
