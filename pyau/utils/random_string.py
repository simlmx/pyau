#
# Generates a random string or arbitrary length
#
# Simon Lemieux
# march 25th 2010
#

from numpy.random import randint

def random_string( length, chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    ''' Returns a string of length 'length' made of random characters from 'chars'.
    '''
    s = ''
    nb_char = len(chars)
    for i in range(length):
        s = s + chars[randint(nb_char)]
    
    return s
        
