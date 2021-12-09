import numpy as np
a = [0,0,2]
b = np.array([2,0,0])

print(np.cross(a,b))
print(np.linalg.norm(np.cross(a,b)))
print(np.cross(a,b) / np.linalg.norm(np.cross(a,b)))
c = np.hstack(([0],a,b))
print("ccc",c)
c = (a-b)/np.linalg.norm(a-b)
print(c)
print(np.cross(c,c))
print(a[:1])