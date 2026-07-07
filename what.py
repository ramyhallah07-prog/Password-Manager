import time

i = 0
for _ in range(10):
    i+=1
    print(i, end = '\r')
    time.sleep(1)