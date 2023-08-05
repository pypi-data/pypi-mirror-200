from typing import Dict, List, Tuple, Union

import bcrypt
import pymysql
import sqlite3


class OpenPySQL:
    """A class used to represent an open connection to a SQL database.

    Attributes
    ----------
    connection : object
        The connection object to the SQL database.
    engine : str
        The engine used for the SQL database (e.g. 'sqlite' or 'mysql').
    cursor : object
        The cursor object for executing queries on the SQL database.

    Methods
    -------
    sqlite(filepath: str) -> 'OpenPySQL'
        Class method that creates an OpenPySQL instance using a SQLite database.
    mysql(user: str, password: str, database: str, host: str = 'localhost', port: int = 3306) -> 'OpenPySQL'
        Class method that creates an OpenPySQL instance using a MySQL database.
    fetch(size: int = 1) -> Union[List[Dict], Dict, None]
        Fetches rows from the result set of a query.
    execute() -> None
        Executes a query on the SQL database and commits changes.
    close() -> None
        Closes the connection to the SQL database.
    """

    def __init__(self, connection: object, engine: str):
        """Constructs all necessary attributes for an OpenPySQL instance.

        Parameters
        ----------
        connection : object
            The connection object to the SQL database.
        engine : str
            The engine used for the SQL database (e.g. 'sqlite' or 'mysql').
        """
        self.connection = connection
        self.engine = engine
        if self.engine == 'sqlite':
            self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    @classmethod
    def sqlite(cls, filepath: str) -> 'OpenPySQL':
        """Class method that creates an OpenPySQL instance using a SQLite database.

        Parameters
        ----------
        filepath : str
            The file path to the SQLite database.

        Returns
        -------
        OpenPySQL
            An OpenPySQL instance connected to the SQLite database.
        """
        connection = sqlite3.connect(filepath)
        return cls(connection, 'sqlite')

    @classmethod
    def mysql(
        cls, user: str,
        password: str,
        database: str,
        host: str = 'localhost',
        port: int = 3306
    ) -> 'OpenPySQL':
        """Class method that creates an OpenPySQL instance using a MySQL database.

        Parameters
        ----------
        user : str
            The username for the MySQL database.
        password : str
            The password for the MySQL database.
        database : str
            The name of the MySQL database to use.
        host : str (optional)
            The hostname or IP address of the MySQL server. Defaults to 'localhost'.
        port : int (optional)
            The port number to use for the connection. Defaults to 3306.

        Returns
        -------
        OpenPySQL
            An OpenPySQL instance connected to the MySQL database.
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

    @staticmethod
    def hashpw(password: str) -> str:
        """Hashes a password using the bcrypt algorithm.

        Parameters
        ----------
        password : str
            The password to hash.

        Returns
        -------
        str
            The hashed password.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=13)).decode()

    @staticmethod
    def checkpw(password: str, hashed: str) -> bool:
        """Checks if a password matches a hashed password.

        Parameters
        ----------
        password : str
            The password to check.
        hashed : str
            The hashed password to check against.

        Returns
        -------
        bool
            True if the password matches the hashed password,
            False otherwise.
        """
        return bcrypt.checkpw(password.encode(), hashed.encode())

    @property
    def query(self) -> str:
        """Gets the query attribute.

        Returns
        -------
        str
            The query attribute.
        """
        return self._query

    @query.setter
    def query(self, query: str) -> None:
        """Sets the query attribute.

        Parameters
        ----------
        query : str
            The new value for the query attribute. If the engine is 'mysql',
            all occurrences of '?' in the query are replaced with '%s'.

        Returns
        -------
        None
        """
        if self.engine == 'mysql':
            query = query.replace('?', '%s')
        self._query = query

    @property
    def value(self) -> Tuple[Union[int, str], ...]:
        """Gets the value attribute.

        Returns
        -------
        Tuple[Union[int, str], ...]
            The value attribute.
        """
        return self._value

    @value.setter
    def value(self, value: Union[int, str, List, Tuple, None]) -> None:
        """Sets the value attribute.

        Parameters
        ----------
        value : Union[int, str, List[Tuple], Tuple[Tuple], None]
            The new value for the value attribute. If value is an integer or string,
            it is converted to a tuple with one element. If value is a list,
            it is converted to a tuple. If value is None or not provided,
            the value attribute is set to an empty tuple.

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

    def fetch(self, size: int = 1) -> Union[List[Dict], Dict, None]:
        """Fetches rows from the result set of a query.

        Parameters
        ----------
        size : int
            The number of rows to fetch. If size is 0, all rows are fetched.
            If size is 1 (default), only one row is fetched.

        Returns
        -------
        Union[List[Dict], Dict, None]
            A list of dictionaries representing the fetched rows if size is 0,
            a dictionary representing the fetched row if size is 1,
            or None if no rows were fetched.
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
        """Executes a query on the SQL database and commits changes.

        If the value attribute is set and its first element is a string or integer,
        the query is executed with the value attribute as a parameter.
        Otherwise, if the value attribute is set and its first element is not a string or integer,
        the executemany method is called with the query and value attributes as parameters.
        If the value attribute is not set, the query is executed without parameters.

        After executing the query, changes are committed to the SQL database.

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
        """Closes the connection to the SQL database.

        Returns
        -------
        None
        """
        self.connection.close()
