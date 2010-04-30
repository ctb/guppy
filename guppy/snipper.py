import sqlite3

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

        CREATE TABLE locations (position INTEGER PRIMARY KEY, seqid TEXT)

        ''')
        self.conn.commit()

    def __len__(self):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM locations')

        return c.fetchone()[0]

    def __contains__(self, locus):
        (seqid, position) = locus

        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM locations WHERE seqid=? and position=?',
                  (seqid, position))

        return c.fetchone()[0]

    def interval_test(self, seqid, start, stop):
        try:
            self.get(seqid, start, stop).next()
        except StopIteration:
            return False

        return True

    def add(self, seqid, position, cursor=None):
        if cursor is None:
            c = self.conn.cursor()
        else:
            c = cursor

        c.execute('REPLACE INTO locations (position, seqid) VALUES (?, ?)',
                  (position, seqid))

        if cursor is None:
            self.conn.commit()

    def get(self, seqid, start, stop):
        c = self.conn.cursor()
        c.execute('SELECT position FROM locations WHERE position >= ? AND position <= ? AND seqid=? ORDER BY position', (start, stop, seqid,))

        for position, in c:
            yield position

    def all(self):
        c = self.conn.cursor()
        c.execute('SELECT seqid, position FROM locations ORDER BY seqid, position')

        for seqid, position in c:
            yield seqid, position

if __name__ == '__main__':
    import sys
    snp_db = SnipperDB(sys.argv[1])

    snp_db.add('foo', 1)
    snp_db.add('foo', 5)

    for x in snp_db.get('foo', 0, 100):
        print x

    for y in snp_db.all():
        print y

    print 'XX', ('foo', 1) in snp_db
    print 'YY', ('foo', 2) in snp_db

    print 'ZZ', snp_db.interval_test('foo', 0, 3)
    print 'ZZ', snp_db.interval_test('foo', 6, 12)
