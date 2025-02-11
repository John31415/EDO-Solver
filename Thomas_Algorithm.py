import numpy as np

# A-Subdiagonal
# B-Diagonal principal
# C-Superdiagonal
# D-Terminos independientes

def thomas_algorithm(A, B, C, D):
    n=len(B)
    c=np.zeros(n-1)
    d=np.zeros(n)
    if n>1:
        c[0]=C[0]/B[0]
    d[0]=D[0]/B[0]
    for i in range(1,n):
        m=B[i]-A[i-1]*c[i-1]
        if i<n-1:
            c[i]=C[i]/m
        d[i]=(D[i]-A[i-1]*d[i-1])/m
    x=np.zeros(n)
    x[-1]=d[-1]
    for i in reversed(range(n-1)):
        x[i]=d[i]-c[i]*x[i+1]
    return x