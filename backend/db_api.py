import peewee
from peewee import *

conn = SqliteDatabase('sovkombank_db')


class BaseModel(Model):
    class Meta:
        database = conn


class Role(BaseModel):
    role_id = AutoField(column_name='user_id')
    name_role = TextField(column_name='name_role', null=False)


class User(BaseModel):
    user_id = AutoField(primary_key=True, column_name='user_id', unique=True,
                        constraints=[peewee.SQL('AUTO_INCREMENT')])
    login = TextField(column_name='login', null=False)
    password = BlobField(column_name='password', null=False)
    role_id = ForeignKeyField(Role, backref='users'),
    salt = BlobField(column_name='salt')

    class Meta:
        table_name = 'users'


cursor = conn.cursor()


def get_user_by_id(id):
    return User.get(User.user_id == id)

def get_user_by_login(login):
    return User.select().where(User.login == login).execute()

def create_user(login, password, role, salt):
    User.create(login=login, password=password, role_id=role, salt = salt)


def delete_user(id):
    User.delete().where(User.user_id == id).execute()


conn.close()
