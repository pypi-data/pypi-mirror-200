import unittest
import sqlite3
from pathlib import Path

from ubercode.utils import cursor

class TestCursor(unittest.TestCase):
    # we will start with the default dict for a new django install
    BASE_DIR = Path(__file__).resolve().parent

    # -------- common usages ----------
    def test_cursor(self):
        with sqlite3.connect(self.BASE_DIR / 'example.db') as conn:
            # create our table
            cur = conn.cursor()
            sql = """
            drop table if exists test;
            """
            cur.execute(sql)
            sql = """
    create table test(
        id INTEGER PRIMARY KEY,
        code TEXT NOT NULL UNIQUE,
        keyword TEXT NOT NULL
        ); """
            sql_select_changes = """
    select changes()
            """
            cur.execute(sql)
            # insert some values as a script (note: will only return the updated value for the last execution step)
            sql = """
    insert into test (code, keyword) values ('test1', 'keyword1');
    insert into test (code, keyword) values ('test2', 'keyword2');
    insert into test (code, keyword) values ('test3', 'keyword3');
            """
            cur.executescript(sql)
            results = cur.execute(sql_select_changes)
            values = cursor.to_values(results)
            # test cursor -> values list
            print(f"last executed statement in script updated: {values}")
            self.assertEqual(values[0], 1)
            # use prepared statement with parameters (note: can show the updated value for each execution step
            sql = "insert into test (code, keyword) values (:code, :keyword);"
            cur.execute(sql, {'code': 'test4', 'keyword': 'keyword4'})
            results = cur.execute(sql_select_changes)
            values = cursor.to_values(results)
            print(f"prepared statement updated: {values}")
            self.assertEqual(values[0], 1)
            cur.execute(sql, {'code': 'test5', 'keyword': 'keyword5'})
            results = cur.execute(sql_select_changes)
            values = cursor.to_values(results)
            print(f"prepared statement updated: {values}")
            self.assertEqual(values[0], 1)
            # query our values
            sql = """
    select * from test;
                    """
            results = cur.execute(sql)
            # test cursor to dicts
            dicts_list = cursor.to_dicts(results)
            print(dicts_list)
            self.assertEqual(dicts_list[0]['id'], 1)
            results = cur.execute(sql)
            # test cursor to tuples
            tuples_list = cursor.to_tuples(results)
            print(tuples_list)
            self.assertEqual(tuples_list[0].id, 1)
