# encoding:utf-8
import yaml


class Database:
    """从config/database.yml读取数据库的基本信息
    """
    def __init__(self) -> None:
        with open('config/database.yml', 'rb') as f:
            info = yaml.load(f, Loader=yaml.FullLoader)
        self.host = info['database']['host']
        self.user = info['database']['user']
        self.password = info['database']['password']
        self.database = info['database']['database']
