import sqlite3
from os.path import exists

# 链接数据库
class DataBase():
    def __init__(self):
        if not exists("user.db"):
            self.connection = sqlite3.connect("user.db")
            self.cursor = self.connection.cursor()
            self.create()
        else:
            self.connection = sqlite3.connect("user.db")
            self.cursor = self.connection.cursor()
        self.is_reset = False

    def execute(self, r, *args, **kwargs):
        self.cursor.execute(r, *args, **kwargs)

    def fetchall(self):
        return self.cursor.fetchall()

    def save(self):
        self.connection.commit()

    # 创建数据库命令
    def create(self):
        r = '''CREATE TABLE user
        (name TEXT primary key, score INTEGER, time INTEGER)'''
        self.execute(r)
        self.save()

    # 重置数据库
    def reset(self):
        if self.is_reset:
            self.execute("drop table user")
            self.create()
            self.save()
            self.is_reset = False

