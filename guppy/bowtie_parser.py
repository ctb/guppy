"""Bowtie parser.

See http://bowtie-bio.sourceforge.net/manual.shtml#algn_out

read(fp) is the main function provided by this module.
"""

import csv
import urllib

DELIMITER='\t'
FIELDNAMES = ['readname', 'strand', 'seqid', 'start', 'read', 'readqual', '_',
              'mismatches']

class Bag(dict):
    """dict-like class that supports attribute access as well as getitem.

    >>> x = Bag()
    >>> x['foo'] = 'bar'
    >>> x.foo
    'bar'
    
    """
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)
        for k in self.keys():
            self.__dict__[k] = self.__getitem__(k)

    def __setitem__(self, k, v):
        dict.__setitem__(self, k, v)
        self.__dict__[k] = v

def read(fp):
    """Parse the given fp as Bowtie output, yielding Bag objects.
    """
    
    reader = csv.DictReader(fp, delimiter=DELIMITER, fieldnames=FIELDNAMES)

    for row in reader:
        # store values in a Bag instead of a dict
        row_d = Bag(row)

        # convert start to int
        row_d['start'] = int(row_d['start'])

        # done!
        yield row_d

if __name__ == '__main__':
    import doctest
    doctest.testmod()
