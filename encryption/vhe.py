from utils.numTh import *
import decimal
from utils.primes import *

decimal.getcontext().prec = 300


class VHE:

    def __init__(self, l, w, bound, stdev, g):
        self.l = l
        self.w = None
        self.bound = bound
        self.stdev = stdev
        self.g = g
        self.w = w

    def setCoeffs(self, array, g = None):
        tarray = array.flatten()
        if g == None:
            g = self.g
        for i in range(len(tarray)):
            tarray[i] = tarray[i] % g
            if tarray[i] > g / 2:
                tarray[i] = tarray[i] - g
        tarray = tarray.reshape(array.shape)
        return tarray

    def get_random_matrix(self, row, col, bound=None):
        if bound == None:
            bound = self.bound
        th = int(pow(2, 31))
        R = np.ones((row, col), np.int).astype(np.object)
        while bound >= th:
            R = np.multiply(R, np.random.randint(-th, th, (row, col)).astype(np.object))
            bound /= th
        R = np.multiply(R, np.random.randint(-bound, bound, (row, col)).astype(np.object))
        return R.astype(np.object)

    # returns S
    def get_secret_key(self, T):
        rows, cols = T.shape
        I = np.eye(rows, dtype=np.int64)
        S = np.hstack((I, T))
        S = S.astype(np.object)
        return S, I

    # returns c*
    def get_bit_vector(self, c):

        result = np.array([bin(int(elem)).replace('b', '').zfill(self.l)[::-1] for elem in c])

        ans = np.zeros((self.l * len(c)), np.int)

        for i, string in enumerate(result):
            string = list(string)
            negate = 1
            if string[-1] == "-":
                string[-1] = '0'
                negate = -1
            for j, char in enumerate(string):
                ans[i * self.l + j] = int(char) * negate

        return ans

    # finds c* then returns Mc*
    def key_switch(self, M, c):
        cstar = self.get_bit_vector(c)
        c_ = np.dot(M, cstar)
        return c_

    # returns S*w
    def get_bit_matrix(self, S):
        powers = np.array([2 ** x for x in range(self.l)])
        result = np.array([np.array([powers * int(elem) for elem in row]) for row in S])
        result = result.reshape(result.shape[0], result.shape[1] * result.shape[2])
        return result

    def key_switch_matrix(self, S, T):
        t_rows, t_cols = T.shape
        s_star = self.get_bit_matrix(S)
        s_rows, s_cols = s_star.shape
        A = self.get_random_matrix(t_cols, s_cols, pow(2, 40))
        E = gauss_sample(s_rows * s_cols, self.stdev)
        E = E.reshape((s_rows, s_cols))
        M = np.vstack((s_star + E - np.matmul(T, A), A))
        return M

    def get_public_key(self, S, T):
        M = self.key_switch_matrix(S, T)
        return M

    def encrypt(self, M, x):
        N = len(x)
        k = np.random.randint(0, self.bound, N).astype(np.object)
        e = gauss_sample(N, self.stdev).astype(np.object)
        sc = self.g * self.w * k + x * self.w + e

        return self.key_switch(M, sc)

    def decrypt(self, S, c):
        sc = np.dot(S, c)
        for i in range(len(sc)):
            sc[i] = int(decimal.Decimal(sc[i]) / decimal.Decimal(self.w) + decimal.Decimal(0.5))
        sc = self.setCoeffs(sc)

        return sc

    def encrypt_image(self, img, N, M):
        H, W, _ = img.shape
        eimg = np.zeros((H, W, 2 * N), np.object)
        for y in range(H):
            for x in range(W):
                t = img[y, x].tolist()
                t.insert(0, 0)
                t = np.asarray(t)
                t = t.astype(np.object)
                eimg[y, x] = self.encrypt(M, t)
        return eimg

    def decrypt_image(self, eimg, S):
        H, W, _ = eimg.shape
        img = np.zeros((H, W, 3), np.uint8)
        for y in range(H):
            for x in range(W):
                img[y, x] = self.decrypt(S, eimg[y, x])[1:4]
        return img

    def rand_decrypt_image(self, eimg, S):
        """
            sc = np.dot(S, c)
            for i in range(len(sc)):
                sc[i] = int(decimal.Decimal(sc[i]) / decimal.Decimal(self.w) + decimal.Decimal(0.5))
            sc = self.setCoeffs(sc)
        """
        H, W, _ = eimg.shape
        img = np.zeros((H, W, 4), np.object)
        for y in range(H):
            for x in range(W):
                sc = np.dot(S, eimg[y, x])
                for i in range(len(sc)):
                    sc[i] = decimal.Decimal(sc[i]) / decimal.Decimal(self.w) + decimal.Decimal(0.5)
                img[y, x] = sc
        return img


if __name__ == "__main__":

    N = 4
    stdev = 3.2
    w = pow(2, 30)
    bound = 200
    l = 100
    g = 0

    while g < pow(2,30):
        g = generate_prime(31)

    v = VHE(l, w, bound, stdev, g)
    T = v.get_random_matrix(N, N)
    S, I = v.get_secret_key(T)
    M = v.get_public_key(I, T)

    p = np.array((15, -2200, -31000, -7), np.object)
    cp = v.encrypt(M, p)
    print(v.decrypt(S, cp))


