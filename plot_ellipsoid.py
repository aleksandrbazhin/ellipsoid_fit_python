import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ellipsoid_fit import ellipsoid_fit, ellipsoid_plot, data_regularize


if __name__=='__main__':

    data = np.loadtxt("mag_out.txt")
    data2 = data_regularize(data, divs=8)

    center, evecs, radii, v = ellipsoid_fit(data2)

    data_centered = data - center.T
    data_centered_regularized = data2 - center.T

    a, b, c = radii
    r = (a * b * c) ** (1. / 3.)
    D = np.array([[r/a, 0., 0.], [0., r/b, 0.], [0., 0., r/c]])
    #http://www.cs.brandeis.edu/~cs155/Lecture_07_6.pdf
    #affine transformation from ellipsoid to sphere (translation excluded)
    TR = evecs.dot(D).dot(evecs.T)
    data_on_sphere = TR.dot(data_centered_regularized.T).T

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    #hack  for equal axes
    # ax.set_aspect('equal')
    # for direction in (-1, 1):
    #     for point in np.diag(direction * np.max(data) * np.array([1, 1, 1])):
    #         ax.plot([point[0]], [point[1]], [point[2]], 'w')
            
    ax.scatter(data_centered[:,0], data_centered[:,1], data_centered[:,2], marker='o', color='g')
    # ax.scatter(data_centered_regularized[:, 0], data_centered_regularized[:, 1],
    #            data_centered_regularized[:, 2], marker='o', color='b')
    ax.scatter(data_on_sphere[:, 0], data_on_sphere[:, 1],
               data_on_sphere[:, 2], marker='o', color='r')

    ellipsoid_plot([0, 0, 0], radii, evecs, ax=ax, plot_axes=True, cage_color='g')
    ellipsoid_plot([0, 0, 0], [r, r, r], evecs, ax=ax, plot_axes=True, cage_color='orange')

    #ax.plot([r],[0],[0],color='r',marker='o')
    #ax.plot([radii[0]],[0],[0],color='b',marker='o')

    plt.show()


