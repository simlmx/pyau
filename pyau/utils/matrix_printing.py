#
# Utils for printing matrices in the console
# I use it for bad printing via ssh when I cannot use matplotlib!
#
# Simon Lemieux
# april 20th 2010
#

from numpy import max, min

def print_matrix(matrix, pixels=' .o0'):
    """ Prints a matrix... """
    matrix = matrix.copy().astype('float')
    max_ = max(matrix)
    max_ = 1.0001*max_ # so we don't hit the max
    min_ = min(matrix)

    matrix -= min_
    matrix /= max_ - min_
        
    nb_pixels = len(pixels)
    
    for row in matrix:
        for el in row:
            idx = int(el*nb_pixels)
            print pixels[idx],
        print


            
    
