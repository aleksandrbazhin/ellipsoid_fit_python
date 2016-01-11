import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ellipsoid_fit import ellipsoid_fit, ellipsoid_plot, data_regularize


if __name__=='__main__':

    data = np.loadtxt("mag_out.txt")
    data2 = data_regularize(data, divs=8)

    center, radii, evecs, v = ellipsoid_fit(data2)

    dataC = data - center.T
    dataC2 = data2 - center.T

    a,b,c = radii
    r = (a*b*c)**(1./3.)#preserve volume?
    D = np.array([[r/a,0.,0.],[0.,r/b,0.],[0.,0.,r/c]])
    #http://www.cs.brandeis.edu/~cs155/Lecture_07_6.pdf
    #affine transformation from ellipsoid to sphere (translation excluded)
    TR = evecs.dot(D).dot(evecs.T)
    dataE = TR.dot(dataC2.T).T

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    

    #hack  for equal axes
    ax.set_aspect('equal')
    MAX = 200
    for direction in (-1, 1):
        for point in np.diag(direction * MAX * np.array([1,1,1])):
            ax.plot([point[0]], [point[1]], [point[2]], 'w')
            
    #ax.scatter(dataC[:,0], dataC[:,1], dataC[:,2], marker='o', color='g')
    ax.scatter(dataC2[:,0], dataC2[:,1], dataC2[:,2], marker='o', color='b')
    ax.scatter(dataE[:,0], dataE[:,1], dataE[:,2], marker='o', color='r')

    ellipsoid_plot([0,0,0], radii, evecs, ax=ax, plotAxes=True, cageColor='g')
    ellipsoid_plot([0,0,0], [r,r,r], evecs,ax=ax, plotAxes=True,cageColor='orange')

    #ax.plot([r],[0],[0],color='r',marker='o')
    #ax.plot([radii[0]],[0],[0],color='b',marker='o')
    #print np.array([radii[0],0,0]).dot(transform)[0], r

    plt.show()


