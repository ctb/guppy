import sqlite3

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

    def add(self, seqid, position, a, c, g, t, cursor=None):
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

if __name__ == '__main__':
    import sys
    snp_db = SnipperDB(sys.argv[1])

    snp_db.add('foo', 1, 'C')
    snp_db.add('foo', 5, 'T')

    for x in snp_db.get('foo', 0, 100):
        print x

    for y in snp_db.all():
        print y
