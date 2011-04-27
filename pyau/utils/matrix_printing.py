#
# Utils for printing matrices in the console
# I use it for bad printing via ssh when I cannot use matplotlib!
#
# Simon Lemieux


# april 20th 2010
#

from numpy import max, min, array

DEFAULT_PIXELS = ' .-+o0#'

def print_matrix(matrix, pixels=DEFAULT_PIXELS):
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


def print_image(file_path, resize = (80,-1) ,pixels=DEFAULT_PIXELS):
    """ Prints an image in the console.
        resize = (x,y), x _or_ y can be -1
                    None for original
    """
    import Image
    
    im = Image.open(file_path)
    size = im.size
    
    if resize is not None:
        resize = list(resize)
        if resize[0] == -1:
            resize[0] = int(round( size[0]*resize[1]/size[1] ))
        elif resize[1] == -1:
            resize[1] = int(round( size[1]*resize[0]/size[0] ))
        im = im.resize(resize)
        size = resize
        
    im = im.convert('F') # black and white
    data = im.getdata()
    x = array(data).reshape(size[::-1])

    print_matrix(x, pixels)
    
    
