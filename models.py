from peewee import *
import datetime
database_proxy = DatabaseProxy()

class BaseModel(Model):
    class Meta:
        database = database_proxy

class History(BaseModel):
    date = DateTimeField(default=datetime.datetime.now)
    src_amount = IntegerField()
    tgt_amount = IntegerField()
    src_currency = CharField()
    tgt_currency = CharField()
    result = FloatField()