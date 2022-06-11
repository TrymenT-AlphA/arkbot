# encoding:utf-8
import yaml

from .Singleton import Singleton


@Singleton
class Database:

    def __init__(self) -> None:
        with open('config.yml', 'r', encoding='utf8') as f:
            info = yaml.load(f, Loader=yaml.FullLoader)['database']
        self.host = info['host']
        self.user = info['user']
        self.password = info['password']
        self.database = info['database']
