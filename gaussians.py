import scipy.stats as st
import numpy as np

def Gaussian:
    def __init__(self, data):
        self.data = data
    def compute(self):
        data = self.data
        if len(data) == 1: return self.gaussian1D(data)
        if len(data) == 2: return self.gaussian2D(data)
        return self.gaussian3D(data)
    def _maxmins(self, X):
        dX = (max(X) - min(X))/10
        xmin = min(X) - dX
        xmax = max(X) + dX
        return xmin, xmax
    # Compute Gaussian in 1d
    def gaussian1D(self, X):
        xmin, xmax = self._maxmins(X)
        kernel = st.gaussian_kde(X)
        xs = np.arange(xmin, xmax, 0.1)
        f = np.reshape(kernel(xs), xs.shape)
        return xs, f
    # Compute Gaussian in 2d
    def gaussian2D(self, X):
        X, Y = X
        xmin, xmax = self._maxmins(X)
        ymin, ymax = self._maxmins(Y)
        xs, ys = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([xs.ravel(), ys.ravel()])
        values = np.vstack([X, Y])
        kernel = st.gaussian_kde(values)
        f = np.reshape(kernel(positions).T, xs.shape)
        return xs, ys, f
    # Compute Gaussian in 3d
    def gaussian3D(self, X):
        X, Y, Z = X
        xmin, xmax = self._maxmins(X)
        ymin, ymax = self._maxmins(Y)
        zmin, zmax = self._maxmins(Z)
        xs, ys, zs = np.mgrid[xmin:xmax:100j, ymin:ymax:100j, zmin:zmax:100j]
        positions = np.vstack([xs.ravel(), ys.ravel(), zs.ravel()])
        values = np.vstack([X, Y, Z])
        kernel = st.gaussian_kde(values)
        f = np.reshape(kernel(positions).T, xs.shape)
        return xs, ys, zs, f