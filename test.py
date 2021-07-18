import numpy as np
n = 10
s1 = np.arange(n)
i_s = (np.random.choice(n,3, replace = False))
i_s.sort()
[i,j,k]= i_s
print(i_s)
s1[i:k+1] = np.roll(s1[i:k+1],k-j)
print(s1)