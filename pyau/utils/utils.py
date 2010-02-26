"""
Misc useful methods.
Feel free to add methods that you often use
"""
def closestPower(n):
    """
    Finds the smallest power of 2 that is >= n
    To optimize FFTs, array lengths should be powers of 2
    """
    power=1
    while (n>power):
        power*=2
    return power  