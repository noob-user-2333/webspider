import dbProxy
from datetime import datetime
from dbProxy import *
from peewee import  *

class WebPage(BaseModel):
    url = CharField()  # 网址
    html = TextField() # 网页HTML内容（长文本）
    timestamp = DateTimeField(default=datetime.now)
dbProxy.db_proxy.create_tables([WebPage])  # 创建表格