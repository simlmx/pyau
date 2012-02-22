#
# february 22nd 2010
# Simon Lemieux
#

from numpy import array, hstack, ones
from numpy.linalg import solve

def fit_parabola(points):
    """ 'points' must be of the form ((x0, y0), (x1, y1), (x2, y2))
        we return a,b,c such that if f(x) = a*x**2 + b*x + c, then
        f(x0)=y0, f(x1)=y1, f(x2)=y2, i.e. the parabola that passes threw the points.
        
        TODO : throw something when the three points are //
    """
    xs = points[:,0]
    ys = points[:,1]
    
    A = hstack([ xs.reshape(3,1) **n for n in [2,1]] +  [ ones(3).reshape(3,1) ])
    
    X = solve(A,ys)
    a,b,c = X.flatten()
    
    return a,b,c
