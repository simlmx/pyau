#
# february 22nd 2010
# Simon Lemieux
#

from numpy import array
from numpy.linalg import solve

def fit_parabola(points):
    """ 'points' must be of the form ((x0, y0), (x1, y1), (x2, y2))
        we return a,b,c such that if f(x) = a*x**2 + b*x + c, then
        f(x0)=y0, f(x1)=y1, f(x2)=y2, i.e. the parabola that passes threw the points.
        
        TODO : throw something when the three points are //
    """
    xs = [x[0] for x in points]
    ys = [x[1] for x in points]
    
    A = array([[ x**n for n in [2,1,0] ] for x in xs])
    B = array(ys)
    
    X = solve(A,B)
    a,b,c = X.flatten()
    
    return a,b,c