import numpy as np
def OneDimension2ThreeDimension(A):
    out = np.zeros((5, 5, 64), dtype = int)
    for i in range(5):
        for j in range(5):
            for k in range(64):
                out[i][j][k] = A[64(5*j + i) + k]
    return out

def theta(A):
    C = np.zeros((5,64), dtype = int)
    for i in range(5):
        for k in range(64):
            for j in range(5):
                C[i][k] ^= A[i][j][k] 

    D =  np.zeros((5,64), dtype = int)
    for i in range(5):
        for k in range(64):
            D[i][k] = C[pow(i-1,1,5),k]^C[pow(i+1,1,5),pow(k-1,1,64)]

    out = np.zeros((5,5,64), dtype = int)
    for i in range(5):
        for j in range(5):
            for k in range(64):
                out[i][j][k] = A[i][j][k]^D[i][k]
    return out
