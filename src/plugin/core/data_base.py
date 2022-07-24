"""数据库
"""
from typing import Optional
import pymysql
from ..utils import json_to_obj
from ..utils import obj_to_json_str
from ..utils import json_str_to_obj


class MySQL:
    """提供数据库操作
    """

    def __init__(self) -> None:
        """初始化
        """
        self._db = None
        self._cursor = None
        _ = json_to_obj('config.json')['database']
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
        assert self._db
        self._cursor = self._db.cursor()

    def _close(self) -> None:
        """关闭连接
        """
        if self._cursor:
            self._cursor.close()
        if self._db:
            self._db.close()

    def _commit(self) -> None:
        """提交修改
        """
        if self._db:
            self._db.commit()
        self._close()

    def fetch_one(self) -> Optional[tuple]:
        """获取一条结果

        返回值:
            Optional[tuple]: 第一条结果
        """
        if not self._cursor:
            return
        return self._cursor.fetchone()

    def fetch_all(self) -> Optional[tuple]:
        """获取所有结果

        返回值:
            Optional[tuple]: 所有结果
        """
        if not self._cursor:
            return
        return self._cursor.fetchall()

    def execute(
            self,
            sql: str,
            args: Optional[tuple] = None
    ) -> int:
        """执行SQL语句

        参数:
            sql: SQL语句
            args: SQL语句的参数

        返回值:
            int: 更新的行数
        """
        self._connect()
        res = self._cursor.execute(sql, args)
        self._commit()
        return res

    def execute_many(
            self,
            sql: str,
            args: tuple
    ) -> int:
        """执行多个SQL语句

        参数:
            sql: SQL语句
            args: SQL语句的参数

        返回值:
            int: 更新的行数
        """
        assert args
        self._connect()
        res = self._cursor.executemany(sql, args)
        self._commit()
        return res

    def select_one(
            self,
            table: str,
            keys: tuple,
            condition: str,
            args: Optional[tuple] = None
    ) -> Optional[dict]:
        """执行一条select语句

        参数:
            table: 表名
            keys: 键
            condition: 条件
            args: 条件的参数

        返回值:
            Optional[dict]: 查询到的数据
        """
        sql = f"""
            SELECT {','.join([f"`{_}`" for _ in keys])}
            FROM `{table}` WHERE {condition};
            """
        if args:
            args = tuple(map(obj_to_json_str, args))
        self.execute(sql, args)
        res = self.fetch_one()
        if not res:
            return
        return dict(zip(keys, map(json_str_to_obj, res)))

    def select_all(
            self,
            table: str,
            keys: tuple,
    ) -> Optional[tuple]:
        """执行一条select语句

        参数:
            table: 表名
            keys: 键
            condition: 条件
            args: 条件的参数

        返回值:
            Optional[tuple]: 查询到的数据
        """
        sql = f"""
            SELECT {','.join([f"`{_}`" for _ in keys])}
            FROM `{table}`;
            """
        self.execute(sql)
        tmp = self.fetch_all()
        if not tmp:
            return
        res = []
        for i, _ in enumerate(tmp):
            res.append(dict(zip(keys, map(json_str_to_obj, _))))
        return tuple(res)

    def update(
            self,
            table: str,
            keys: tuple,
            vals: tuple,
            condition: str,
            args: Optional[tuple] = None
    ) -> int:
        """执行一条select语句

        参数:
            table: 表名
            keys: 键
            vals: 值
            condition: 条件
            args: 条件的参数

        返回值:
            int: 更新的条数
        """
        assert len(keys) == len(vals)
        sql = f"""
            UPDATE `{table}` SET
            {','.join([f"`{_}`=%s" for _ in keys])}
            WHERE {condition}
            """
        args = tuple(map(obj_to_json_str, vals + args))
        return self.execute(sql, args)

    def insert(
            self,
            table: str,
            keys: tuple,
            vals: tuple
    ) -> int:
        """执行一条insert语句

        参数:
            table: 表名
            keys: 键
            vals: 值

        返回值:
            int: 更新的行数
        """
        assert len(keys) == len(vals)
        sql = f"""
            INSERT INTO `{table}`
            ({','.join([f"`{_}`" for _ in keys])}) 
            VALUES
            ({','.join(['%s' for _ in vals])});
            """
        args = tuple(map(obj_to_json_str, vals))
        return self.execute(sql, args)

    def delete(
            self,
            table: str,
            condition: str,
            args: Optional[tuple] = None
    ) -> int:
        """执行一条delete语句

        参数:
            table: 表名
            condition: 条件
            args: 条件的参数

        返回值:
            int: 更新的行数
        """
        sql = f"""
            DELETE FROM `{table}`
            WHERE {condition}
            """
        args = tuple(map(obj_to_json_str, args))
        return self.execute(sql, args)
