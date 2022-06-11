# encoding:utf-8
from typing import Any

import pymysql

from ..utils import load_yaml


class Database:

    def __init__(self) -> None:
        self.db = None
        self.cursor = None
        info = load_yaml('config.yml')['database']
        self.host = info['HOST']
        self.user = info['USER']
        self.password = info['PASSWORD']
        self.database = info['DATABASE']

    def _connect(self) -> None:
        self.db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database)
        if self.db is None:
            raise RuntimeError('cannot connect to database!')
        self.cursor = self.db.cursor()

    def _close(self) -> None:
        if self.cursor is not None:
            self.cursor.close()
        if self.db is not None:
            self.db.close()

    def _commit(self) -> None:
        if self.db is not None:
            self.db.commit()
        self._close()

    def execute(self, sql: str, args: tuple or list or None) -> None:
        self._connect()
        try:
            if args is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, args)
        except:
            self.db.rollback()
            raise RuntimeError('execute error')
        finally:
            self._commit()

    def fetchone(self) -> Any:
        if self.cursor is None:
            raise RuntimeError('fetch before execute!')
        return self.cursor.fetchone()

    def fetchall(self) -> Any:
        if self.cursor is None:
            raise RuntimeError('fetch before execute!')
        return self.cursor.fetchall()
