
import numpy as np 
from datetime import datetime
import time 


# A = np.array([[1, 2, 3]])
# B = np.array([[1.1, 2.9, 6.0]])

# print(A-B)


# t1 = datetime.now()
# time.sleep(0.1)
# t2 = datetime.now()

# # print(type(t2-t1))
# t = t2- t1
# print(t.total_seconds())


a = np.zeros([1,3])

b = np.array([1,2,3])
ab = [a,b]


# print(ab[1])
b[:-1] = b[1:]
print(b)