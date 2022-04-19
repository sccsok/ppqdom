# -*- coding: utf-8 -*


class Quaternion:

    def add(self, quater1, quater2):
        q = [0,0,0,0]
        for i in range(4):
            q[i] = quater1[i] + quater2[i]
        return q

    def sub(self, quater1, quater2):
        q = [0,0,0,0]
        for i in range(4):
            q[i] = quater1[i] - quater2[i]
        return q

    def nmul(self, quater, number):
        return [number*quater[0],number*quater[1],number*quater[2],number*quater[3]]

    def mul(self, quater1, quater2):
        q = quater1.copy()
        p = quater2.copy()
        s = q[0] * p[0] - q[1] * p[1] - q[2] * p[2] - q[3] * p[3]
        x = q[0] * p[1] + q[1] * p[0] + q[2] * p[3] - q[3] * p[2]
        y = q[0] * p[2] - q[1] * p[3] + q[2] * p[0] + q[3] * p[1]
        z = q[0] * p[3] + q[1] * p[2] - q[2] * p[1] + q[3] * p[0]
        return [s, x, y, z]

    def divide(self, quater1, quater2):
        """右除"""
        result = self.mul(quater1, self.inverse(quater2))
        return result

    def modpow(self, quater):
        """模的平方"""
        q = quater.copy()
        result = q[0]
        for i in range(1, 4):
            result += q[i] ** 2
        return result

    def mod(self, quater):
        """求模"""
        return pow(self.modpow(), 1 / 2)

    def conj(self, quater):
        """转置"""
        q = quater.copy()
        for i in range(1, 4):
            q[i] = -q[i]
        return [q[0], q[1], q[2], q[3]]

    def inverse(self, quater):
        """求逆"""
        q = quater.copy()
        mod = self.modpow()
        for i in range(4):
            q[i] /= mod
        return [q[0], -q[1], -q[2], -q[3]]



