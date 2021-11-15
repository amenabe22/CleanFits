import datetime
import peewee as pw
import peeweedbevolve
from playhouse.migrate import *
from peewee_migrate import Router
from peewee import SqliteDatabase
from .settings import DB_NAME, DB_HOST, DB_PASS, DB_USER

# from crud.core import

database = pw.PostgresqlDatabase(
    DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
# migrator = PostgresqlMigrator(database=database)


class BaseModel(Model):
    class Meta:
        database = database


class BotUser(BaseModel):
    username = pw.CharField(max_length=300)
    first_name = pw.CharField(max_length=200)
    bot_id = pw.BigIntegerField(unique=True)
    email = pw.CharField(max_length=200, null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    verified = pw.BooleanField(default=False)


class Store(BaseModel):
    store_name = pw.CharField(max_length=300)
    user = ForeignKeyField(BotUser, backref='store')
    timestamp = pw.DateTimeField(default=datetime.datetime.now)


# class User(BaseModel):
#     username = TextField()


# class Tweet(BaseModel):
#     content = TextField()
    # timestamp = DateTimeField(default=datetime.now)
#     user = ForeignKeyField(User, backref='tweets')


# class Favorite(BaseModel):
    # user = ForeignKeyField(User, backref='favorites')
#     tweet = ForeignKeyField(Tweet, backref='favorites')

# def run_migrations():
#     # Create migration
#     router.create('migration_name')

#     # Run migration/migrations
#     router.run('migration_name')

#     # Run all unapplied migrations
#     router.run()


def create_tables():
    # db.evolve()
    database.evolve()
    # database.create_tables([BotUser])
