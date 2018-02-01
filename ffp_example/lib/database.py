from peewee import *
db = SqliteDatabase('test.db')
class Room(Model):
    Name = CharField()
    Code = CharField()

    class Meta:
        database = db
class Cabinet(Model):
    Phsics_num = CharField()
    room_id = ForeignKeyField(Room, related_name='room')


db.create_tables([Room,Cabinet])