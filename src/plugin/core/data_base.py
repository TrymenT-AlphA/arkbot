# encoding:utf-8
"""数据库类,提供数据库操作
"""
from typing import Iterable
import pymysql
from ..utils import yaml_to_obj


class Database:
    """数据库类,提供数据库操作
    """
    def __init__(self) -> None:
        """读取配置
        """
        self._db = None # 用于连接数据库
        self._cursor = None # 用于操作数据库
        _ = yaml_to_obj('config.yml')['database'] # 数据库配置信息
        self._host = _['HOST']
        self._user = _['USER']
        self._password = _['PASSWORD']
        self._database = _['DATABASE']

    def _connect(self) -> None:
        """连接数据库,获取cursor

        异常抛出:
            RuntimeError: 无法连接数据库
        """
        self._db = pymysql.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            database=self._database)
        if self._db is None:
            raise RuntimeError('无法连接到数据库')
        self._cursor = self._db.cursor()

    def _close(self) -> None:
        """关闭数据库连接
        """
        if self._cursor is not None:
            self._cursor.close()
        if self._db is not None:
            self._db.close()

    def _commit(self) -> None:
        """提交所作的修改
        """
        if self._db is not None:
            self._db.commit()
        self._close()

    def get_host(self) -> str:
        """获取当前数据库HOST
        """
        return self._host

    def get_user(self) -> str:
        """获取当前数据库USER
        """
        return self._user

    def get_password(self) -> str:
        """获取当前数据库PASSWORD
        """
        return self._password

    def get_database(self) -> str:
        """获取当前数据库DATABASE
        """
        return self._database

    def execute(self, sql: str, args : Iterable or None = None) -> int:
        """执行一条SQL语句

        参数:
            sql (str): SQL语句
            args (tupleorlistorNone): 传入参数. 默认为None

        返回值:
            int: 受影响的行数
        """
        self._connect()
        res = self._cursor.execute(sql, args)
        self._commit()
        return res

    def executemany(self, sql: str, args: Iterable[Iterable]) -> int:
        """一次性执行一系列SQL语句,必须传入参数

        参数:
            sql (str): SQL语句
            argslist (Iterable[Iterable]): 一系列参数. 默认为None

        返回值:
            int: 受影响的行数
        """
        if args is not None:
            self._connect()
            res = self._cursor.executemany(sql, args)
            self._commit()
            return res
        else:
            return 0

    def execute_script(self, path: str) -> None:
        """执行SQL脚本,每条命令独占一行

        参数:
            path (str): SQL脚本路径
        """
        with open(path, 'r', encoding='utf8') as _:
            for sql in _.readlines():
                self._cursor.execute(sql.strip())

    def fetchone(self) -> tuple or None:
        """获取一条结果

        返回值:
            tuple or None: 一条结果
        """
        if self._cursor is not None:
            return self._cursor.fetchone()
        return None

    def fetchall(self) -> Iterable[Iterable] or None:
        """获取所有结果

        返回值:
            Iterable[Iterable] or None: 所有结果
        """
        if self._cursor is not None:
            return self._cursor.fetchall()
        return None
