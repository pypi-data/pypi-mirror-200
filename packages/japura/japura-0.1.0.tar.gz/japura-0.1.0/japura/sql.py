from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

import pymysql
import sqlite3


class SQL:
    """A class that provides a simple interface for executing SQL queries and managing database connections.

    Parameters
    ----------
    connection : object
        A database connection object that is used to interact with the database.
    engine : str
        The type of database engine being used. Valid values are "sqlite" and "mysql".

    Methods
    -------
    sqlite(filename: str) -> SQL:
        Create a new instance of the SQL class using a SQLite database file.

    mysql(user: str, password: str, database: str, host: Optional[str] = 'localhost', port: Optional[int] = 3306) -> SQL:
        Create a new instance of the SQL class using a MySQL database connection.

    fetch(size: Optional[int] = 1) -> Union[List[Dict], Dict, None]:
        Executes the currently set query and value, returns the result(s) based on the specified size.

    execute() -> None:
        Executes the currently set query and value, commits any changes to the database.

    close() -> None:
        Closes the database connection.

    Properties
    ----------
    query : str
        The SQL query to be executed.

    value : Tuple[Union[int, str], ...]
        The values to be substituted into the query.
    """

    def __init__(self, connection: object, engine: str):
        """Initialize a new instance of the SQL class with the given database connection and engine.

        Parameters
        ----------
        connection : object
            A database connection object that is used to interact with the database.

        engine : str
            The type of database engine being used. Valid values are "sqlite" and "mysql".
        """
        self.connection = connection
        self.engine = engine
        if self.engine == 'sqlite':
            self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    @classmethod
    def sqlite(cls, filename: str) -> 'SQL':
        """Create a new instance of the SQL class using a SQLite database file.

        Parameters
        ----------
        filename : str
            The path to the SQLite database file.

        Returns
        -------
        SQL
            A new instance of the SQL class with a connection to the SQLite database file.
        """
        connection = sqlite3.connect(filename)
        return cls(connection, 'sqlite')

    @classmethod
    def mysql(
        cls, user: str,
        password: str,
        database: str,
        host: Optional[str] = 'localhost',
        port: Optional[int] = 3306
    ) -> 'SQL':
        """Create a new instance of the SQL class using a MySQL database connection.

        Parameters
        ----------
        user : str
            The username used to connect to the MySQL database.

        password : str
            The password used to connect to the MySQL database.

        database : str
            The name of the MySQL database to connect to.

        host : Optional[str]
            The hostname or IP address of the MySQL server (default is 'localhost').

        port : Optional[int]
            The port number used to connect to the MySQL server (default is 3306).

        Returns
        -------
        SQL
            A new instance of the SQL class with a connection to the MySQL database.
        """
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor,
        )
        return cls(connection, 'mysql')

    @property
    def query(self) -> str:
        return self._query

    @query.setter
    def query(self, query: str) -> None:
        """Set the SQL query string associated with this SQL instance.

        This method also performs any necessary formatting of the query string based on the database engine being used.

        Parameters
        ----------
        query : str
            The SQL query string to associate with this SQL instance.

        Returns
        -------
        None
        """
        if self.engine == 'mysql':
            query = query.replace('?', '%s')
        self._query = query

    @property
    def value(self) -> Tuple[Union[int, str], ...]:
        return self._value

    @value.setter
    def value(self, value: Union[int, str, None, Iterable[Any]]) -> None:
        """Set the parameter values associated with this SQL instance.

        This method also performs any necessary formatting of the parameter values based on their types.

        Parameters
        ----------
        value : Union[int, str, None, Iterable[Any]]
            The parameter values to associate with this SQL instance.

        Returns
        -------
        None
        """
        if value:
            if any(isinstance(value, t) for t in [int, str]):
                value = (value,)
            if isinstance(value, List):
                value = tuple(value)
        self._value = value or ()

    def fetch(self, size: Optional[int] = 1) -> Union[List[Dict], Dict, None]:
        """Executes the currently set query and value, returns the result(s) based on the specified size.

        Parameters
        ----------
        size : Optional[int]
            The number of rows to fetch.

            `size=0` fetches all rows and returns a list of dictionaries.

            `size=1` fetches a single row and returns a dictionary.

        Returns
        -------
        Union[List[Dict], Dict, None]
            A list of dictionaries (`size=0`), a dictionary (`size=1`), or `None`.
        """
        self.cursor.execute(self.query, self.value)
        if self.engine == 'mysql':
            if size == 0:
                return self.cursor.fetchall()
            elif size == 1:
                return self.cursor.fetchone()
            else:
                raise ValueError
        elif self.engine == 'sqlite':
            exec = self.cursor.execute(self.query, self.value)
            if size == 0:
                if res := exec.fetchall():
                    return [{k: r[k] for k in r.keys()} for r in res]
            elif size == 1:
                if res := exec.fetchone():
                    return {k: res[k] for k in res.keys()}
            else:
                raise ValueError

    def execute(self) -> None:
        """Executes the currently set query and value, commits any changes to the database.

        Returns
        -------
        None
        """
        if self.value:
            if any(isinstance(self.value[0], t) for t in [str, int]):
                self.cursor.execute(self.query, self.value)
            else:
                self.cursor.executemany(self.query, self.value)
        else:
            self.cursor.execute(self.query)
        self.connection.commit()

    def close(self) -> None:
        """Closes the database connection.

        Returns
        -------
        None
        """
        self.connection.close()
