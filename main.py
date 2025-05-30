from dbProxy import *
from peewee import *
# 定义模型
class TestData(BaseModel):
    id = AutoField()
    data = TextField()  # 约16KB数据
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        database = None
