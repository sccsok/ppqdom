from utils.numTh import *
import decimal

decimal.getcontext().prec = 60


class OldVHE:

    def __init__(self, l, bound, stdev, q, w):
        self.l = l
        self.bound = bound
        self.stdev = stdev
        self.q = q
        self.w = w

    def setCoeffs(self, array):
        tarray = array.flatten()
        for i in range(len(tarray)):
            tarray[i] = tarray[i] % self.q
            if tarray[i] > self.q / 2:
                tarray[i] = tarray[i] - self.q
        tarray = tarray.reshape(array.shape)
        return tarray

    def setCoeffs_(self, array):
        tarray = array.flatten()
        for i in range(len(tarray)):
            tarray[i] = tarray[i] % self.q
        tarray = tarray.reshape(array.shape)
        return tarray

    def get_random_matrix(self, row, col, bound=None):
        if bound == None:
            bound = self.bound
        R = np.random.randint(-bound, bound, (row, col))
        R = R.astype(np.object)
        return R

    # returns S
    def get_secret_key(self, T):
        rows, cols = T.shape
        I = np.eye(cols, dtype=np.int64)
        return np.hstack((I, T)), I

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
        c_ = self.setCoeffs(c_)
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
        A = self.get_random_matrix(t_cols, s_cols, pow(2, 31))
        E = gauss_sample(s_rows * s_cols, self.stdev)
        E = E.reshape((s_rows, s_cols))
        E = E.astype(np.object)
        M = np.vstack((s_star + E - np.matmul(T, A), A))
        return M

    def get_public_key(self, S, T):
        M = self.key_switch_matrix(S, T)
        return M

    def encrypt(self, M, x):
        x = x.astype(np.object)
        sc = x * self.w
        return self.key_switch(M, sc)

    def decrypt(self, S, c):
        sc = np.dot(S, c)
        for i in range(len(sc)):
            sc[i] = int(round(decimal.Decimal(sc[i]) / decimal.Decimal(self.w)))
        sc = self.setCoeffs(sc)

        return sc

    def encrypt_image(self, img, M):
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


if __name__ == "__main__":

    N = 4
    stdev = 3.2
    w = pow(2, 30)
    bound = 100
    l = 100
    q = pow(2, 50)

    v = OldVHE(l, bound, stdev, q, w)
    T = v.get_random_matrix(N, N)
    S, I = v.get_secret_key(T)
    # print("secret kry: \n", S)
    M = v.get_public_key(I, T)

    p = np.array((15,-2200,-31000,-7), np.object)
    cp = v.encrypt(M, p)
    print(v.decrypt(S, cp))


