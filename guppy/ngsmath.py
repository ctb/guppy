import math

def calc_entropy(a, c, g, t):
    total = float(sum((a, c, g, t)))
    ps = [ float(x) / float(total) for x in (a, c, g, t) ]
    entropy = -sum([ p*math.log(p, 2) for p in ps if p ])

    return entropy

def calc_dot_product(acgt1, acgt2):
    """
    >>> x = calc_dot_product([1,1,1,1], [1,1,1,1])
    >>> assert x == 1, x

    >>> x = calc_dot_product([1,0,1,0], [0,1,0,1])
    >>> assert x == 0, x

    >>> x = calc_dot_product([5,5,5,5], [1,1,1,1])
    >>> assert x == 1, x

    >>> x = calc_dot_product([5,5,5,5], [6,6,6,6])
    >>> assert x == 1, x
    """
    
    len1 = math.sqrt(sum([ x**2 for x in acgt1 ]))
    len2 = math.sqrt(sum([ x**2 for x in acgt2 ]))

    if len1 == 0 or len2 == 0:
        return 0.0

    acgt1 = [ float(x) / len1 for x in acgt1 ]
    acgt2 = [ float(x) / len2 for x in acgt2 ]

    prod = math.sqrt(sum([ (x*y) for (x, y) in zip(acgt1, acgt2) ]))

    return prod

def max_snp(a, c, g, t):
    m = max((a, c, g, t))
    if a == m: return 'A'
    if c == m: return 'C'
    if g == m: return 'G'
    if t == m: return 'T'
    assert False

