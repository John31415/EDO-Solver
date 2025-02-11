import numpy as np
from Thomas_Algorithm import thomas_algorithm

def f(a, b, c, d, x):
    return (a+b*x+c*x**2+d*x**3)

def polynomial(a, b, c, d, X):
    x=[]
    y=[]
    itx=(X[-1]-X[0])/500
    x_val=X[0]
    pos=1
    for i in range(500):
        x.append(x_val)
        if x_val>X[pos]:
            pos+=1
        y.append(f(a[pos-1],b[pos-1],c[pos-1],d[pos-1],x_val-X[pos-1]))
        x_val+=itx
    return x,y


def cubic_splines(x, y):
    x=np.asarray(x, dtype=float)
    y=np.asarray(y, dtype=float)
    n=len(x)
    if n<3:
        return [], [], False
    h=np.diff(x)
    A=np.zeros(n-2)
    for i in range(n-2):
        A[i]=h[i]
    B=np.zeros(n-2)
    for i in range(n-2):
        B[i]=2*(h[i]+h[i+1])
    C=np.zeros(n-2)
    for i in range(n-2):
        C[i]=h[i+1]
    D=np.zeros(n-2)
    for i in range(1,n-1):
        D[i-1]=6*((y[i+1]-y[i])/h[i]-(y[i]-y[i - 1])/h[i-1])
    m=np.zeros(n)
    m[1:-1]=thomas_algorithm(A,B,C,D)
    a=np.zeros(n-1)
    for i in range(n-1):
        a[i]=y[i]
    b=np.zeros(n-1)
    for i in range(n-1):
        b[i]=(y[i+1]-y[i])/h[i]-h[i]*(2*m[i]+m[i+1])/6
    c=np.zeros(n-1)
    for i in range(n-1):
        c[i]=m[i]/2
    d=np.zeros(n-1)
    for i in range(n-1):
        d[i]=(m[i+1]-m[i])/(6*h[i])
    q,w=polynomial(a,b,c,d,x)
    return q,w,True