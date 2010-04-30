"""Bowtie parser.

See http://bowtie-bio.sourceforge.net/manual.shtml#algn_out

read(fp) is the main function provided by this module.
"""

import csv
import urllib
from recordtype import recordtype

DELIMITER='\t'
FIELDNAMES = ['readname', 'strand', 'seqid', 'start', 'read', 'readqual',
              'n_mismatches', 'mismatches']

RawBowtieLine = recordtype('RawBowtieLine', FIELDNAMES)

def read(fp):
    """Parse the given fp as Bowtie output, yielding Bag objects.
    """
    
    reader = csv.DictReader(fp, delimiter=DELIMITER, fieldnames=FIELDNAMES)

    for row in reader:
        # store values in a Bag instead of a dict
        row_d = RawBowtieLine(**row)

        # convert start to int
        row_d.start = int(row_d.start)

        # done!
        yield row_d

if __name__ == '__main__':
    import doctest
    doctest.testmod()
