# encoding:utf-8
"""数据库类
"""
from typing import Iterable, Optional, Any
import pymysql
from ..utils import yaml_to_obj


class Database:
    """提供数据库操作
    """

    def __init__(self) -> None:
        """初始化数据库
        """
        self._db = None
        self._cursor = None
        _ = yaml_to_obj('config.yml')['database']
        self._host = _['HOST']
        self._user = _['USER']
        self._password = _['PASSWORD']
        self._database = _['DATABASE']

    def _connect(self) -> None:
        """建立连接
        """
        self._db = pymysql.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            database=self._database
        )
        if self._db is None:
            raise RuntimeError('无法连接到数据库')
        self._cursor = self._db.cursor()

    def _close(self) -> None:
        """关闭连接
        """
        if self._cursor is not None:
            self._cursor.close()
        if self._db is not None:
            self._db.close()

    def _commit(self) -> None:
        """提交修改
        """
        if self._db is not None:
            self._db.commit()
        self._close()

    def execute(self, sql: str, args: Optional[Iterable] = None) -> int:
        """执行SQL语句

        参数:
            sql (str): SQL语句
            args (Optional[Iterable]): 可选参数

        返回值:
            int: 受影响的行数
        """
        self._connect()
        res = self._cursor.execute(sql, args=args)
        self._commit()
        return res

    def executemany(self, sql: str, args: Iterable[Any]) -> int:
        """执行多个SQL语句

        参数:
            sql (str): SQL语句
            args (Iterable[Any]): 一系列参数
        返回值:
            int: 受影响的行数
        """
        assert args is not None
        self._connect()
        res = self._cursor.executemany(sql, args)
        self._commit()
        return res

    def execute_script(self, path: str) -> None:
        """执行SQL脚本,每条命令独占一行

        参数:
            path (str): SQL脚本路径
        """
        with open(path, 'r', encoding='utf8') as _tmp:
            for sql in _tmp.readlines():
                self._cursor.execute(sql.strip())

    def fetchone(self) -> Optional[tuple]:
        """获取一条结果

        返回值:
            Optional[tuple]: 一条结果
        """
        if self._cursor is not None:
            return self._cursor.fetchone()
        return None

    def fetchall(self) -> Optional[Iterable[Iterable]]:
        """获取所有结果

        返回值:
            Optional[Iterable[Iterable]]: 所有结果
        """
        if self._cursor is not None:
            return self._cursor.fetchall()
        return None
