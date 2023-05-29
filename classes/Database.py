import sqlite3

class Database:

    dbfile = 'datas/blog.db'

    @staticmethod
    def query_db(query, args=()):
        conn = sqlite3.connect(Database.dbfile)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        cur.close()

        rv = [{k: m[k] for k in m.keys()} for m in rv]
        return rv

    @staticmethod
    def commit_bd(query, args):
        conn = sqlite3.connect(Database.dbfile)
        cur = conn.cursor()
        cur.execute(query, args)
        conn.commit()
        cur.close()
        