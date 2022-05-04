import numpy as np
import cv2
from polynomials.hahn import ha_poly
from polynomials.tchebichef import tch_ploy


class Moment:

    def __init__(self, npoly, mpoly):
        self.npoly = npoly
        self.mpoly = mpoly

    def gray_moment(self, image, npoly=None, mpoly=None):
        """
        Input a gray image
        Output image moments
        """
        if npoly is not None:
            self.npoly = npoly

        if mpoly is not None:
            self.mpoly = mpoly

        return np.dot(np.dot(self.npoly, image), self.mpoly.T)

    def inv_gray_moment(self, moments, n, m, npoly=None, mpoly=None, flag=True):
        """
        Input orders(n, m)
        OutPut reconstructed image
        """

        if npoly is not None:
            self.npoly = npoly

        if mpoly is not None:
            self.mpoly = mpoly

        part_hahn_moments = moments[0:n, 0:m]
        height, width = moments.shape

        t_hahn_moments = np.pad(part_hahn_moments, ((0, height - n), (0, width - m)), 'constant', constant_values=(0, 0))
        recons_image = self.npoly.T.dot(t_hahn_moments.dot(self.mpoly))

        return np.round(recons_image).astype(np.uint8) if flag else recons_image

    def qua_moment(self, color_image, npoly=None, mpoly=None):
        """
        Input color_image
        Output quaternion hahn moments
        """

        if npoly is not None:
            self.npoly = npoly

        if mpoly is not None:
            self.mpoly = mpoly

        height, width, _ = color_image.shape
        r_channel_moment = self.gray_moment(color_image[:, :, 0])
        g_channel_moment = self.gray_moment(color_image[:, :, 1])
        b_channel_moment = self.gray_moment(color_image[:, :, 2])

        qua_moments = np.zeros((height, width, 4))
        A_0 = (r_channel_moment + g_channel_moment + b_channel_moment) / np.sqrt(3)
        A_1 = (g_channel_moment - b_channel_moment) / (-np.sqrt(3))
        A_2 = (b_channel_moment - r_channel_moment) / (-np.sqrt(3))
        A_3 = (r_channel_moment - g_channel_moment) / (-np.sqrt(3))

        for p in range(height):
            for q in range(width):
                qua_moments[p, q] = [A_0[p, q], A_1[p, q], A_2[p, q], A_3[p, q]]

        return qua_moments

    def inv_qua_moment(self, qua_moments, n, m):
        """
        Input orders(n, m)
        OutPut reconstructed color image
        """
        height, width, _ = qua_moments.shape

        A0 = qua_moments[:, :, 0]
        A1 = qua_moments[:, :, 1]
        A2 = qua_moments[:, :, 2]
        A3 = qua_moments[:, :, 3]

        a1 = (1 / np.sqrt(3)) * (
                    self.inv_gray_moment(A0, n, m, flag=False) + self.inv_gray_moment(A2, n, m, flag=False)
                    - self.inv_gray_moment(A3, n, m, flag=False))
        a2 = (1 / np.sqrt(3)) * (
                    self.inv_gray_moment(A0, n, m, flag=False) - self.inv_gray_moment(A1, n, m, flag=False)
                    + self.inv_gray_moment(A3, n, m, flag=False))
        a3 = (1 / np.sqrt(3)) * (
                    self.inv_gray_moment(A0, n, m, flag=False) + self.inv_gray_moment(A1, n, m, flag=False)
                    - self.inv_gray_moment(A2, n, m, flag=False))

        recons_image = np.zeros((height, width, 3), np.uint8)

        for y in range(height):
            for x in range(width):
                t = [a1[y, x], a2[y, x], a3[y, x]]
                recons_image[y, x] = np.asarray(t)

        return recons_image


if __name__ == '__main__':
    a = 10
    b = 10
    image = cv2.imread('../data/baboon.ppm')
    if image.shape[0] > 256:
        image = cv2.resize(image, (256, 256))
    h, w, _ = image.shape
    cv2.imshow("src", image)
    # m = Moment(ha_poly(h), ha_poly(w))
    m = Moment(tch_ploy(h), tch_ploy(w))
    # m = Moment(kra_ploy(h), kra_ploy(w))
    moments = m.qua_moment(image)
    dst_image = m.inv_qua_moment(moments, 256, 256)
    cv2.imshow("dst", dst_image)
    cv2.waitKey()