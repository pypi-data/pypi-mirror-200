# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's database methods.
"""


from typing import Any, List, Dict, Iterable, Optional, Literal, Union, ClassVar, NoReturn, overload
from re import findall
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Engine, Connection
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.elements import TextClause

from .rbasic import get_first_notnull
from .rdata import to_table, distinct
from .rmonkey import add_result_more_fetch, support_row_index_by_field
from . import roption
from .rregular import res
from .rtext import rprint
from .rdatetime import now
from .rwrap import runtime

# Version compatible of package sqlalchemy.
try:
    from sqlalchemy import CursorResult
except ImportError:
    from sqlalchemy.engine.cursor import LegacyCursorResult as CursorResult


# Monkey patch.
add_result_more_fetch()
support_row_index_by_field()

class RConnect(object):
    """
    Rey's database connection type, based on the package sqlalchemy.
    """

    # Values to be converted to None.
    none_values: ClassVar[List] = ["", " ", b"", [], (), {}, set()]

    @overload
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        url: Optional[Union[str, URL]] = None,
        conn: Optional[Union[Engine, Connection]] = None,
        autocommit: bool = True,
        recreate_ms: int = 7_200_000,
        **query: str
    ) -> None: ...

    @overload
    def __init__(self, username: None, url: None, conn: None) -> NoReturn: ...

    @overload
    def __init__(self, password: None, url: None, conn: None) -> NoReturn: ...

    @overload
    def __init__(self, host: None, url: None, conn: None) -> NoReturn: ...

    @overload
    def __init__(self, port: None, url: None, conn: None) -> NoReturn: ...

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        drivername: Optional[str] = None,
        url: Optional[Union[str, URL]] = None,
        conn: Optional[Union[Engine, Connection]] = None,
        autocommit: bool = True,
        recreate_ms: int = 7_200_000,
        **query: str
    ) -> None:
        """
        Set database connection parameters.

        Parameters
        ----------
        username : Server user name.
        password : Server password.
        host : Server host.
        port : Server port.
        database : Database name in the server.
        drivername : Database backend and driver name.
        url: Server connection URL, will get parameters from it, but preferred input or connection parameters.
        conn : Existing connection object, will get parameters from it, but preferred input parameters.
        autocommit : Whether the auto commit for execution.
        recreate_ms : Connection object recreate interval millisecond.
        query : Connection parameters.
        """

        # Extract parameters from URL.
        if url != None:

            ## from str object.
            if type(url) == str:
                pattern = "^([\w\+]+)://(\w+):(\w+)@(\d+\.\d+\.\d+\.\d+):(\d+)[/]?(\w+)?[\?]?([\w&=]+)?$"
                url_params = res(url, pattern)
                if url_params == None:
                    raise ValueError("the value of parameter 'url' is incorrect")
                else:
                    url_drivername, url_username, url_password, url_host, url_port, url_database, url_query_str = url_params
                    if url_query_str != None:
                        pattern = "(\w+)=(\w+)"
                        url_query_findall = findall(pattern, url_query_str)
                        url_query = {key: val for key, val in url_query_findall}

            ## from URL object.
            elif type(url) == URL:
                url_drivername = url.drivername
                url_username = url.username
                url_password = url.password
                url_host = url.host
                url_port = url.port
                url_database = url.database
                url_query = dict(url.query)

        else:
            url_drivername, url_username, url_password, url_host, url_port, url_database, url_query = (
                None, None, None, None, None, None, {}
            )

        # Extract parameters from existing connection object.
        if conn != None:

            ## Convert to Engine object.
            if type(conn) == Connection:
                engine = conn.engine
            elif type(conn) == Engine:
                engine = conn
                conn = engine.connect()

            ## Extract parameters.
            engine_drivername = engine.url.drivername
            engine_username = engine.url.username
            engine_password = engine.url.password
            engine_host = engine.url.host
            engine_port = engine.url.port
            engine_database = engine.url.database
            engine_query = dict(engine.url.query)

        else:
            engine_drivername, engine_username, engine_password, engine_host, engine_port, engine_database, engine_query = (
                None, None, None, None, None, None, {}
            )

        # Set parameters by priority.
        self.drivername = get_first_notnull(drivername, url_drivername, engine_drivername, default="mysql+mysqldb")
        self.username = get_first_notnull(username, url_username, engine_username, default="error")
        self.password = get_first_notnull(password, url_password, engine_password, default="error")
        self.host = get_first_notnull(host, url_host, engine_host, default="error")
        self.port = get_first_notnull(port, url_port, engine_port, default="error")
        self.database = get_first_notnull(database, url_database, engine_database)
        self.query = get_first_notnull(query, url_query, engine_query, default={}, none_values=[{}])
        self.autocommit = autocommit
        self.conn = conn
        self.begin = None
        self.conn_timestamp = now("timestamp")
        self.recreate_ms = recreate_ms

    def commit(self) -> None:
        """
        Commit cumulative executions.
        """

        # Commit.
        if self.begin != None:
            self.begin.commit()
            self.begin = None

    def rollback(self) -> None:
        """
        Rollback cumulative executions.
        """

        # Rollback.
        if self.begin != None:
            self.begin.rollback()
            self.begin = None

    def close(self) -> None:
        """
        Close database connection.
        """

        # Close.
        if self.conn != None:
            self.conn.close()
            self.conn = None
        self.begin = None

    def url(self, database: Optional[str] = None, **query: str) -> str:
        """
        Get server connection URL.

        Parameters
        ----------
        database : Database name in the server.
        query : Connection parameters.

        Returns
        -------
        Server connection URL.
        """

        # Get parameters by priority.
        database: str = get_first_notnull(database, self.database)
        query: str = get_first_notnull(query, self.query, default={"charset": "utf8"}, none_values=[{}])

        # Create URL.
        _url = f"{self.drivername}://{self.username}:{self.password}@{self.host}:{self.port}"

        # Add database path.
        if database != None:
            _url = f"{_url}/{database}"

        # Add connection parameters.
        if query != {}:
            query = "&".join(
                [
                    "%s=%s" % (key, val)
                    for key, val in query.items()
                ]
            )
            _url = f"{_url}?{query}"

        return _url

    def engine(self, database: Optional[str] = None, **query: str) -> Engine:
        """
        Create database engine object.

        Parameters
        ----------
        database : Database name in the server.
        query : Connection parameters.

        Returns
        -------
        Engine object.
        """

        # Create.
        drivernames = (self.drivername, "mysql+mysqldb", "mysql+pymysql")
        drivernames = distinct(drivernames)
        for drivername in drivernames:
            self.drivername = drivername
            url = self.url(database, **query)
            try:
                engine = create_engine(url)
                return engine
            except ModuleNotFoundError:
                pass

        # Throw error.
        drivernames_str = " and ".join(
            [
                dirvername.split("+", 1)[-1]
                for dirvername in drivernames
            ]
        )
        raise ModuleNotFoundError("module %s not fund" % drivernames_str)

    def connect(self, database: Optional[str] = None, **query: str) -> Connection:
        """
        Create database connection object.

        Parameters
        ----------
        database : Database name in the server.
        query : Connection parameters.

        Returns
        -------
        Connection object.
        """

        # Check whether the connection object is invalid.
        if self.conn != None and (
            now("timestamp") > self.conn_timestamp + self.recreate_ms \
            or self.conn.closed
        ):
            self.close()

        # Judge whether existing connection objects can be reused.
        elif self.conn != None and (
            database == None or self.conn.engine.url.database == database
        ):
            return self.conn

        # Create connection object.
        engine = self.engine(database, **query)
        conn = engine.connect()

        # Save connection object.
        self.conn = conn
        self.conn_timestamp = now("timestamp")

        return conn

    def fill_data_by_sql(
        self,
        sql: Union[str, TextClause],
        params: Union[Dict, List[Dict]],
        fill_field: bool = True,
        none_values: List = none_values
    ) -> List[Dict]:
        """
        Fill missing parameters according to contents of sqlClause object of sqlalchemy module, and filter out empty Dict.

        Parameters
        ----------
        sql : SQL in sqlalchemy.text format or return of sqlalchemy.text.
        params : Parameters set for filling sqlalchemy.text.
        fill_field : Whether fill missing fields.
        none_values : Values to be converted to None.

        Returns
        -------
        Filled parameters.
        """

        # Handle parameters.
        if type(params) == dict:
            params = [params]

        # Filter out empty Dict.
        params = [
            param
            for param in params
            if param != {}
        ]

        # Extract fill field names.
        if type(sql) == TextClause:
            sql = sql.text
        pattern = "(?<!\\\):(\w+)"
        sql_keys = findall(pattern, sql)

        # Fill.
        for param in params:
            for key in sql_keys:
                if fill_field:
                    val = param.get(key)
                else:
                    val = param[key]
                if val in none_values:
                    val = None
                param[key] = val

        return params

    def execute(
        self,
        sql: Union[str, TextClause],
        params: Optional[Union[List[Dict], Dict]] = None,
        database: Optional[str] = None,
        fill_field: bool = True,
        none_values: List = none_values,
        autocommit: Optional[bool] = None,
        report: bool = False,
        **kw_params: Any
    ) -> CursorResult:
        """
        Execute SQL.

        Parameters
        ----------
        sql : SQL in sqlalchemy.text format or return of sqlalchemy.text.
        params : Parameters set for filling sqlalchemy.text.
        database : Database name.
        fill_field : Whether fill missing fields.
        none_values : Values to be converted to None.
        autocommit : Whether the auto commit for execution.
        report : Whether print SQL and SQL runtime.
        kw_params : Keyword parameters for filling sqlalchemy.text.

        Returns
        -------
        CursorResult object of alsqlchemy package.
        """

        # Get parameters by priority.
        autocommit = get_first_notnull(autocommit, self.autocommit, default=True)

        # Handle parameters.
        if type(sql) == str:
            sql = text(sql)
        if params != None:
            if type(params) == dict:
                params = [params]
            else:
                params = params.copy()
            for param in params:
                param.update(kw_params)
        else:
            params = [kw_params]
        params = self.fill_data_by_sql(sql, params, fill_field, none_values)

        # Get Connection object.
        conn = self.connect(database)

        # Get Transaction object.
        if self.begin == None:
            self.begin = conn.begin()

        # Execute SQL.
        if report:
            result, report_runtime = runtime(conn.execute, sql, params, _ret_report=True)
            report_info = "%s\nRow Count: %d" % (report_runtime, result.rowcount)
            if params == []:
                rprint(report_info, sql, title="SQL", frame=roption.print_default_frame_full)
            else:
                rprint(report_info, sql, params, title="SQL", frame=roption.print_default_frame_full)
        else:
            result = conn.execute(sql, params)

        # Commit execute.
        if autocommit:
            self.commit()

        return result

    def execute_select(
            self,
            table: str,
            database: Optional[str] = None,
            fields: Optional[Union[str, Iterable]] = None,
            where: Optional[str] = None,
            order: Optional[str] = None,
            limit: Optional[Union[int, str, Iterable[Union[int, str]]]] = None,
            report: bool = False
        ) -> CursorResult:
        """
        Execute select SQL.

        Parameters
        ----------
        table : Table name.
        database : Database name.
        fields : Select clause content.
            - None : Is 'SELECT *'.
            - str : Join as 'SELECT str'.
            - Iterable[str] : Join as 'SELECT \`str\`, ...'.

        where : 'WHERE' clause content, join as 'WHERE str'.
        order : 'ORDER BY' clause content, join as 'ORDER BY str'.
        limit : 'LIMIT' clause content.
            - Union[int, str] : Join as 'LIMIT int/str'.
            - Iterable[Union[str, int]] with length of 1 or 2 : Join as 'LIMIT int/str, ...'.

        report : Whether print SQL and SQL runtime.

        Returns
        -------
        CursorResult object of alsqlchemy package.
        """

        # Handle parameters.
        sqls = []
        if database == None:
            _database = self.database
        else:
            _database = database
        if fields == None:
            fields = "*"
        elif type(fields) != str:
            fields = ",".join(["`%s`" % field for field in fields])

        # Generate SQL.
        select_sql = (
            f"SELECT {fields}\n"
            f"FROM `{_database}`.`{table}`"
        )
        sqls.append(select_sql)
        if where != None:
            where_sql = "WHERE %s" % where
            sqls.append(where_sql)
        if order != None:
            order_sql = "ORDER BY %s" % order
            sqls.append(order_sql)
        if limit != None:
            if type(limit) in [str, int]:
                limit_sql = f"LIMIT {limit}"
            else:
                if len(limit) in [1, 2]:
                    limit_content = ",".join([str(val) for val in limit])
                    limit_sql = "LIMIT %s" % limit_content
                else:
                    raise ValueError("The length of the parameter 'limit' value must be 1 or 2")
            sqls.append(limit_sql)
        sql = "\n".join(sqls)

        # Execute SQL.
        result = self.execute(sql, database=database, report=report)

        return result

    def execute_update(
        self,
        data: Union[CursorResult, List[Dict], Dict],
        table: str,
        database: Optional[str] = None,
        where_fields: Optional[Union[str, Iterable[str]]] = None,
        report: bool = False
    ) -> Optional[CursorResult]:
        """
        Update the data of table in the datebase.

        Parameters
        ----------
        data : Updated data.
        table : Table name.
        database : Database name.
        where_fields : 'WHERE' clause content.
            - None : The first key value pair of each item is judged.
            - str : This key value pair of each item is judged.
            - Iterable[str] : Multiple judged, 'and' relationship.

        report : Whether print SQL and SQL runtime.

        Returns
        -------
        None or CursorResult object.
            - None : When the data is empty.
            - CursorResult object : When the data is not empty.
        """

        # Handle parameters.
        if type(data) == CursorResult:
            data = to_table(data)
        elif type(data) == dict:
            data = [data]
        if database == None:
            _database = self.database
        else:
            _database = database

        # If data is empty, not execute.
        if data in ([], [{}]):
            return

        # Generate SQL.
        data_flatten = {}
        sqls = []
        if where_fields == None:
            no_where = True
        else:
            no_where = False
            if type(where_fields) == str:
                where_fields = [where_fields]
        for index, row in enumerate(data):
            for key, val in row.items():
                index_key = "%d_%s" % (index, key)
                data_flatten[index_key] = val
            if no_where:
                where_fields = [list(row.keys())[0]]
            set_content = ",".join(
                [
                    "`%s` = :%d_%s" % (key, index, key)
                    for key in row
                    if key not in where_fields
                ]
            )
            where_content = "\n    AND ".join(
                [
                    f"`{field}` = :{index}_{field}"
                    for field in where_fields
                ]
            )
            sql = (
                f"UPDATE `{_database}`.`{table}`\n"
                f"SET {set_content}\n"
                f"WHERE {where_content}"
            )
            sqls.append(sql)
        sqls = ";\n".join(sqls)

        # Execute SQL.
        result = self.execute(sqls, data_flatten, database, once=False, report=report)

        return result

    def execute_insert(
        self,
        data: Union[CursorResult, List[Dict], Dict],
        table: str,
        database: Optional[str] = None,
        duplicate_method: Optional[Literal["ignore", "update"]] = None,
        report: bool = False
    ) -> Optional[CursorResult]:
        """
        Insert the data of table in the datebase.

        Parameters
        ----------
        data : Updated data.
        table : Table name.
        database : Database name.
        duplicate_method : Handle method when constraint error.
            - None : Not handled.
            - 'ignore' : Use 'UPDATE IGNORE INTO' clause.
            - 'update' : Use 'ON DUPLICATE KEY UPDATE' clause.

        report : Whether print SQL and SQL runtime.

        Returns
        -------
        None or CursorResult object.
            - None : When the data is empty.
            - CursorResult object : When the data is not empty.
        """

        # Handle parameters.
        if type(data) == CursorResult:
            data = self.to_table(data)
        elif type(data) == dict:
            data = [data]
        if database == None:
            _database = self.database
        else:
            _database = database

        # If data is empty, not execute.
        if data in ([], [{}]):
            return

        # Generate SQL.
        fields = list({key for row in data for key in row})
        fields_str = ",".join(["`%s`" % field for field in fields])
        fields_str_position = ",".join([":" + field for field in fields])
        if duplicate_method == "ignore":
            sql = (
                f"INSERT IGNORE INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )
        elif duplicate_method == "update":
            update_content = ",".join(["`%s` = VALUES(`%s`)" % (field, field) for field in fields])
            sql = (
                f"INSERT INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})\n"
                "ON DUPLICATE KEY UPDATE\n"
                f"{update_content}"
            )
        else:
            sql = (
                f"INSERT INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )

        # Execute SQL.
        result = self.execute(sql, data, database, report=report)

        return result