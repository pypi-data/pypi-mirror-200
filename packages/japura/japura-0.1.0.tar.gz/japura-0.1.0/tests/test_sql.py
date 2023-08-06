from japura.sql import SQL

import os


def test_sqlite():

    filename = 'test.db'

    db = SQL.sqlite(filename)

    db.query = "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)"
    db.value = None
    db.execute()

    db.query = "INSERT INTO test_table VALUES (?, ?)"
    db.value = [(1, 'Alice'), (2, 'Bob')]
    db.execute()

    db.query = "SELECT * FROM test_table"
    db.value = None

    result = db.fetch(0)
    assert len(result) == 2
    assert result[0]['id'] == 1
    assert result[0]['name'] == 'Alice'
    assert result[1]['id'] == 2
    assert result[1]['name'] == 'Bob'

    result = db.fetch(1)
    assert result['id'] == 1
    assert result['name'] == 'Alice'

    db.query = "SELECT name FROM test_table WHERE id = ?"
    db.value = 2

    result = db.fetch(size=1)
    assert result['name'] == 'Bob'

    db.close()

    os.remove(filename)
