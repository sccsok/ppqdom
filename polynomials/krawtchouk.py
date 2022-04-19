import numpy as np
import math


def weight(N, p):
    """
    Weight function
    """
    wx = np.zeros(N)
    wx[0] = math.exp((N - 1) * math.log(1 - p) / 2)
    for x in range(1, N):
        wx[x] = math.sqrt((((N - 1) - x + 1) / x) * (p / (1 - p))) * wx[x - 1]
        
    return wx


def kra_ploy(N, p=0.5):
    """
    Krawtchouk polynomials
    """
    kploy = np.zeros((N, N))
    wx = weight(N, p)

    for x in range(0, int(N/2)):

        kploy[0, x] = wx[x]
        kploy[0, N-1-x] = kploy[0, x] / pow(-1, 0)

        kploy[N-1, x] = kploy[0, x] / pow(-1, x)
        kploy[N-1, N-1-x] = kploy[N-1, x] / pow(-1, N-1)

        rho = math.sqrt((1 - p) / (p * (N - 1)))

        kploy[1, x] = (1 - x / (p * (N - 1))) * wx[x] / rho
        kploy[1, N-1-x] = kploy[1, x] / pow(-1, 1)

        kploy[N-2, x] = kploy[1, x] / pow(-1, x)
        kploy[N-2, N-1-x] = kploy[N-2, x] / pow(-1, N-2)

        for n in range(2, int(N/2)):

            A = math.sqrt(-((1-p)*n)/(p*(-(N-1)+(n-1))))
            B = math.sqrt(((1-p)*(1-p)*n*(n-1))/(p*p*(-(N-1)+(n-1))*(-(N-1)+(n-1)-1)))

            kploy[n, x] = (((N-1)-2*(n-1))*p+(n-1)-x)*kploy[n-1,x]/A
            kploy[n, x] = kploy[n, x] - (n-1)*(1-p)*kploy[n-2,x]/B
            kploy[n, x] = kploy[n, x] / (p*((N-1)-(n-1)))

            kploy[n, N-1-x] = kploy[n, x] / pow(-1, n)

            kploy[N-1-n, x] = kploy[n, x] / pow(-1, x)
            kploy[N-1-n, N-1-x] = kploy[N-1-n, x] / pow(-1, N-1-n)

    return kploy


