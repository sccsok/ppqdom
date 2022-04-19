import numpy as np


def tch_ploy(N):
    """
    Tchebichef polynomials
    """
    tpoly = np.zeros((N, N))

    for x in range(0, N):
        tpoly[0, x] = 1 / np.sqrt(N)

    for t in range(1, N):

        tpoly[t, 0] = -np.sqrt((N - t) / (N + t)) * np.sqrt((2 * t + 1) / (2 * t - 1)) * tpoly[t - 1, 0]
        tpoly[t, 1] = (1 + t * (1 + t) / (1 - N)) * tpoly[t, 0]

        tpoly[t, N - 2] = (-1)**t * tpoly[t, 1]
        tpoly[t, N - 1] = (-1)**t * tpoly[t, 0]

        for x in range(2, int(N / 2)):

            g1 = (-t * (t + 1) - (2 * x - 1) * (x - N - 1) - x) / (x * (N - x))
            g2 = ((x - 1) * (x - N - 1)) / (x * (N - x))

            tpoly[t, x] = g1 * tpoly[t, x-1] + g2 * tpoly[t, x-2]

            tpoly[t, N-1-x] = (-1)**t * tpoly[t, x]

    return tpoly