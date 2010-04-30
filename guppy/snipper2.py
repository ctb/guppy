import sqlite3
import csv

ntd = dict(A=0, C=1, G=2, T=3)

class SnipperDB(object):
    def __init__(self, filename, initialize=True):
        self.conn = sqlite3.connect(filename)

        c = self.conn.cursor()
        if initialize:
            try:
                c.execute('DELETE FROM locations')
            except sqlite3.OperationalError:
                self._create_tables(c)
            
        else:
            try:
                c.execute('SELECT * FROM locations LIMIT 1')
            except sqlite3.OperationalError:
                # table doesn't exist -- create
                self._create_tables(c)

    def close(self):
        self.conn.close()

    def sync(self):
        self.conn.commit()
    commit = sync

    def cursor(self):
        return self.conn.cursor()

    def _create_tables(self, c):
        c.execute('''

        CREATE TABLE locations (position INTEGER PRIMARY KEY, seqid TEXT, a INTEGER, c INTEGER, g INTEGER, t INTEGER)

        ''')
        self.conn.commit()

    def __contains__(self, locus):
        (seqid, position) = locus

        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM locations WHERE seqid=? and position=?',
                  (seqid, position))

        return c.fetchone()[0]

    def __len__(self):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM locations')

        return c.fetchone()[0]

    def add_one(self, seqid, position, nt, cursor=None):
        """for example, add_one(seqid, pos, 'a')"""
        self.add(seqid, position, cursor=cursor, **{nt.lower() : 1})

    def add(self, seqid, position, a=0, c=0, g=0, t=0, cursor=None):
        if cursor is None:
            cur = self.conn.cursor()
        else:
            cur = cursor

        cur.execute('SELECT a, c, g, t FROM locations WHERE position=? and seqid=?', (position, seqid))
        results = cur.fetchone()
        if results:
            a0, c0, g0, t0 = results
            results = [a0+a, c0+c, g0+g, t0+t]
        else:
            results = [a,c,g,t]

        results.append(position)
        results.append(seqid)

        cur.execute('REPLACE INTO locations (a, c, g, t, position, seqid) VALUES (?, ?, ?, ?, ?, ?)', results)

        if cursor is None:
            self.conn.commit()

    def get(self, seqid, start, stop):
        c = self.conn.cursor()
        c.execute('SELECT position, a, c, g, t FROM locations WHERE position >= ? AND position <= ? AND seqid=? ORDER BY position', (start, stop, seqid,))

        for x in c:
            yield x

    def all(self):
        c = self.conn.cursor()
        c.execute('SELECT seqid, position, a, c, g, t FROM locations ORDER BY seqid, position')

        for x in c:
            yield x

    def dump_to_csv(self, fp):
        w = csv.writer(fp, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        
        # output to 'alleles.txt' in Excel-able format.
        for (chr, pos, a, c, g, t) in self.all():
            w.writerow((chr, pos, a, c, g, t, a + c + g +t ))

def _test():
    snp_count = SnipperDB(":memory:")

    snp_count.add_one('foo', 1, 'C')
    snp_count.add_one('foo', 5, 'T')
    snp_count.add_one('foo', 1, 'C')
    snp_count.add('foo', 2, a=1, c=1, g=5, t=1)
    snp_count.sync()

    i = iter(snp_count.get('foo', 0, 10))
    x = i.next()
    assert x == (1, 0, 2, 0, 0)         # 2 'C's at position 1
    x = i.next()
    assert x == (2, 1, 1, 5, 1)
    x = i.next()
    assert x == (5, 0, 0, 0, 1)         # 1 'T' at position 5

    return snp_count
    
if __name__ == '__main__':
    import sys

    snp_count = _test()
    print '** test passed'
    snp_count.dump_to_csv(sys.stdout)
