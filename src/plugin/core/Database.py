# encoding:utf-8
import yaml


class Database:

    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self) -> None:
        with open('config/database.yml', 'rb') as f:
            info = yaml.load(f, Loader=yaml.FullLoader)
        self.host = info['database']['host']
        self.user = info['database']['user']
        self.password = info['database']['password']
        self.database = info['database']['database']
