import numpy as np
import cv2
import math


def fc(n):
    """
    Get fiboracci sequence
    """
    if n == 0 or n == 1:
        return 1
    
    else:
        return n * fc(n - 1)


def x_k(x, k):
    """
    Pochhammer symbol
    """
    if k == 1:
        return x

    return (x + k - 1) * x_k(x, k - 1)


def ha_poly(order, a=None, b=None):
    """
    Hahn polynomials
    """
    if a is None and b is None:
        a = 10
        b = 10
        
    hpolys = np.zeros((order, order))
    
    for x in range(0, order):

        hpolys[0, x] = math.sqrt(
            x_k(order - x, a) * x_k(x + 1, b) * fc(a + b + 1) / (fc(a) * fc(b) * x_k(order, a + b + 1)))

    for n in range(1, order):

        hpolys[n, 0] = -math.sqrt((order - n) * (a + n) * (a + b + n) * (2 * n + 1 + a + b) / (
                    n * (2 * n + a + b - 1) * (b + n) * (n + a + b + order))) * hpolys[n - 1, 0]

        hpolys[n, 1] = ((n + b + 1) * (order - n - 1) - n * (order + a - 1)) / ((b + 1) * (order - 1)) * math.sqrt(
            (b + 1) * (order- 1) / (order + a - 1)) * hpolys[n, 0]

        hpolys[n, order - 2] = (-1) ** n * hpolys[n, 1]

        hpolys[n, order - 1] = (-1) ** n * hpolys[n, 0]

        for x in range(2, int(order / 2)):

            g1 = (x - 1) * (order + a - x + 1)
            g2 = (b + 1) * (order - 1) - (a + b + 2) * (x - 1)
            g3 = n * (a + b + n + 1)
            g4 = (2 * g1 + g2 - g3) / (g1 + g2) * math.sqrt((b + x) * (order - x) / ((order + a - x) * x))
            g5 = -g1 / (g1 + g2) * math.sqrt(
                (b + x) * (b + x - 1) * (order - x) * (order - x + 1) / (x * (x - 1) * (order + a - x) * (order + a - x + 1)))

            hpolys[n, x] = g4 * hpolys[n, x - 1] + g5 * hpolys[n, x - 2]

            hpolys[n, order - 1 - x] = (-1) ** n * hpolys[n, x]

    return hpolys
