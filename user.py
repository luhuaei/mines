from database import DataBase


DB = DataBase()

# 用户数据库
class User():
    def __init__(self, name, score, time):
        self.name = name
        self.is_exists_name = False
        self.score = score
        self.time = time

    def user_insert(self):
        if not self.is_exists_name:
            r = '''insert into user values(?, ?, ?)'''
            DB.execute(r, (self.name, self.score, self.time))
            DB.save()

    def user_exists(self):
        r = '''select * from user where name = ?'''
        DB.execute(r, (self.name, ))
        if DB.fetchall():
            self.is_exists_name = True

    def user_delete(self):
        r = '''delete from user where name = ?'''
        DB.execute(r, (self.name, ))
        DB.save()

    def user_update(self):
        r = "update user set score = ? , time = ?, where name = ?"
        DB.execute(r, (self.score, self.time, self.name))
        DB.save()

    def user_query(self):
        if self.is_exists_name:
            r = "select * from user where name = ?"
            DB.execute(r, (self.name, ))
            _, old_score, old_time = DB.fetchall()[0]
            if self.score == old_score:
                if self.time > old_time:
                    self.time = old_time
