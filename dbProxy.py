import atexit
import os
from peewee import *
DB_PATH = "/dev/shm/webspider.db"
if os.name == 'nt':
    DB_PATH = "Z:\\webspider.db"
db = SqliteDatabase(DB_PATH)
db.connect()
# 定义一个全局代理
db_proxy = DatabaseProxy()
db_proxy.initialize(db)
print(f'当前使用数据库为SQLite，地址为:{DB_PATH}')
# 所有 Model 继承自 BaseModel，使用 db_proxy
class BaseModel(Model):
    class Meta:
        database = db_proxy  # 关键：所有 Model 使用同一个代理
def close_db():
    if not db.is_closed():
        db.close()
        print("数据库连接已关闭")
atexit.register(close_db)  # 程序退出时自动调用

__all__ = ["BaseModel"]
