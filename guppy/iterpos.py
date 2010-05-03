def union(iter_a, iter_b, get_position_fn):
    """
    >>> fn = lambda x: x
    
    >>> list_a = [1, 2, 3]
    >>> list_b = [1, 2, 3]
    >>> list(union(list_a, list_b, fn))
    [(1, 1), (2, 2), (3, 3)]

    >>> list_a = [1]
    >>> list_b = [1, 2, 3]
    >>> list(union(list_a, list_b, fn))
    [(1, 1), (None, 2), (None, 3)]
    >>> list(union(list_b, list_a, fn))
    [(1, 1), (2, None), (3, None)]

    >>> list_a = [1, 3]
    >>> list_b = [1, 2]
    >>> list(union(list_a, list_b, fn))
    [(1, 1), (None, 2), (3, None)]
    >>> list(union(list_b, list_a, fn))
    [(1, 1), (2, None), (None, 3)]

    >>> list_a = [2, 3, 4]
    >>> list_b = [3, 4]
    >>> list(union(list_a, list_b, fn))
    [(2, None), (3, 3), (4, 4)]
    >>> list(union(list_b, list_a, fn))
    [(None, 2), (3, 3), (4, 4)]

    >>> list_a = [2, 3, 4, 5]
    >>> list_b = [3, 4]
    >>> list(union(list_a, list_b, fn))
    [(2, None), (3, 3), (4, 4), (5, None)]
    >>> list(union(list_b, list_a, fn))
    [(None, 2), (3, 3), (4, 4), (None, 5)]

    >>> list_a = [1, 3, 5]
    >>> list_b = [2, 4]
    >>> list(union(list_a, list_b, fn))
    [(1, None), (None, 2), (3, None), (None, 4), (5, None)]
    >>> list(union(list_b, list_a, fn))
    [(None, 1), (2, None), (None, 3), (4, None), (None, 5)]

    >>> list_a = []
    >>> list_b = []
    >>> list(union(list_a, list_b, fn))
    []
    >>> list(union(list_b, list_a, fn))
    []

    """
    
    ia = iter(iter_a)
    ib = iter(iter_b)

    val_a = ia.next()
    pos_a = get_position_fn(val_a)
    
    val_b = ib.next()
    pos_b = get_position_fn(val_b)

    exit_a = False
    exit_b = False
    while 1:

        while pos_a != pos_b:
            # catch up to the position for value 'b'
            while pos_a < pos_b:
                yield val_a, None

                try:
                    val_a = ia.next()
                    pos_a = get_position_fn(val_a)
                except StopIteration:
                    yield None, val_b
                    return

            # catch up to the position for value 'a'
            while pos_a > pos_b:
                yield None, val_b

                try:
                    val_b = ib.next()
                    pos_b = get_position_fn(val_b)
                except StopIteration:
                    yield val_a, None
                    return

            # now, we've either swapped (so now pos_a < pos_b again) or they
            # are equal, in which case we break out of the loop.

        # ok, equal -- return a pair.
        yield val_a, val_b

        # advance both iterators simultaneously
        try:
            val_a = ia.next()
            pos_a = get_position_fn(val_a)
        except StopIteration:
            exit_a = True

        try:
            val_b = ib.next()
            pos_b = get_position_fn(val_b)
        except StopIteration:
            exit_b = True

        # did we get a StopIteration of some sort?
        if exit_a or exit_b:
            if not exit_a and exit_b:
                yield val_a, None
                while 1:
                    yield ia.next(), None
            if exit_a and not exit_b:
                yield None, val_b
                while 1:
                    yield None, ib.next()

            return
        
    # done!

if __name__ == '__main__':
    import doctest
    doctest.testmod()
