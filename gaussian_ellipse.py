import numpy as np
import sklearn
import math
from scipy.stats import chi2
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from random import *
from matplotlib.patches import Ellipse
from numpy.linalg import cholesky

# https://github.com/joferkington/oost_paper_code/blob/master/error_ellipse.py
def plot_point_cov(points, nstd=2, ax=None, **kwargs):
    """
    Plots an `nstd` sigma ellipse based on the mean and covariance of a point
    "cloud" (points, an Nx2 array).
    Parameters
    ----------
        points : An Nx2 array of the data points.
        nstd : The radius of the ellipse in numbers of standard deviations.
            Defaults to 2 standard deviations.
        ax : The axis that the ellipse will be plotted on. Defaults to the 
            current axis.
        Additional keyword arguments are pass on to the ellipse patch.
    Returns
    -------
        A matplotlib ellipse artist
    """
    # 计算点的均值和协方差
    pos = points.mean(axis=0)
    cov = np.cov(points, rowvar=False)
    # 画椭圆
    return plot_cov_ellipse(cov, pos, nstd, ax, **kwargs)

def plot_cov_ellipse(cov, pos, nstd=2, ax=None, **kwargs):
    """
    Plots an `nstd` sigma error ellipse based on the specified covariance
    matrix (`cov`). Additional keyword arguments are passed on to the 
    ellipse patch artist.
    Parameters
    ----------
        cov : The 2x2 covariance matrix to base the ellipse on
        pos : The location of the center of the ellipse. Expects a 2-element
            sequence of [x0, y0].
        nstd : The radius of the ellipse in numbers of standard deviations.
            Defaults to 2 standard deviations.
        ax : The axis that the ellipse will be plotted on. Defaults to the 
            current axis.
        Additional keyword arguments are pass on to the ellipse patch.
    Returns
    -------
        A matplotlib ellipse artist
    """
    def eigsorted(cov):
        vals, vecs = np.linalg.eigh(cov)
        order = vals.argsort()[::-1]
        return vals[order], vecs[:,order]

    # 坐标轴
    if ax is None:
        ax = plt.gca()

    # 计算协方差矩阵的特征值和特征向量
    vals, vecs = eigsorted(cov)
    print(vals)
    print(vecs)

    # 计算坐标轴旋转的角度
    theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))
    print(*vecs[:,0][::-1])
    print(np.arctan2(*vecs[:,0][::-1]))
    print(theta)

    # 计算椭圆的长轴和短轴
    # Width and height are "full" widths, not radius
    width, height = 2 * nstd * np.sqrt(vals)
    print(width)
    print(height)

    # 得到椭圆
    ellip = Ellipse(xy=pos, width=width, height=height, angle=theta, **kwargs)

    # 画椭圆
    ax.add_artist(ellip)
    return ellip

# generate a bivariate Gaussian distribution points set
def generate_gaussian(mu, sigma, sample_num = 300):
    # mu = np.array([[1, 5]])
    # sigma = np.array([[1, 0.5], [1.5, 3]])
    # Cholesky 分解是把一个对称正定的矩阵表示成一个下三角矩阵L和其转置的乘积的分解
    R = cholesky(sigma)
    # 生成服从高斯分布的数据
    s = np.dot(np.random.randn(sample_num, 2), R) + mu
    return s
    # plt.plot(s[:,0], s[:,1], 'o')
    # plt.show()

def plot_bivariate_gaussian():
    mu = np.array([[1, 5]])
    sigma = np.array([[0.03, -0.0004], [-0.0004, 0.005]])
    print(sigma)
    s1 = generate_gaussian(mu, sigma)

    # mu = np.array([[4, 11]])
    # sigma = np.array([[2.4, 3.1], [1.5, 3.7]])
    # s2 = generate_gaussian(mu, sigma)

    kwrg = {'edgecolor':'k', 'linewidth':0.5}

    plt.plot(s1[:,0], s1[:,1], 'go')
    # plt.plot(s2[:,0], s2[:,1], 'go')

    plot_point_cov(s1, nstd = 2, alpha = 0.7, color = 'pink', **kwrg)
    # plot_point_cov(s2, nstd = 2, alpha = 0.7, color = 'pink', **kwrg)
    plt.show()

def plot_single_gaussian():
    # 定义高斯1的均值和协方差矩阵
    mu = np.array([[1, 5]])
    sigma = np.array([[1, 0.5], [1.5, 3]])

    # 生成服从高斯分布1的数据（300个点）
    s1 = generate_gaussian(mu, sigma)

    # 定义高斯2的均值和协方差矩阵
    mu = np.array([[4, 11]])
    sigma = np.array([[2.4, 3.1], [1.5, 3.7]])

    # 生成服从高斯分布1的数据（300个点）
    s2 = generate_gaussian(mu, sigma)

    # 将两个高斯分布的点连接起来
    X = np.hstack((s1[:,0], s2[:,0]))
    Y = np.hstack((s1[:,1], s2[:,1]))
    X.shape = (600, 1)
    Y.shape = (600, 1)
    points = np.c_[X,Y]

    kwrg = {'edgecolor':'k', 'linewidth':0.5}

    # 画点
    plt.plot(s1[:,0], s1[:,1], 'go')
    plt.plot(s2[:,0], s2[:,1], 'go')
    # 画协方差
    plot_point_cov(points, nstd = 2, alpha = 0.7, color = 'pink', **kwrg)
    plt.show()

if __name__ == '__main__':
    plot_bivariate_gaussian()
    # plot_single_gaussian()