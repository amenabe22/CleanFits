import datetime
import peewee as pw
from playhouse.migrate import *
from peewee_migrate import Router
from peewee import SqliteDatabase
from .settings import DB_NAME, DB_HOST, DB_PASS, DB_USER
# Make sure this import is below peewee
import peeweedbevolve

# from crud.core import

database = pw.PostgresqlDatabase(
    database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
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
    category = pw.CharField(choices=[('dress', 'Dresses')],null=True)
    has_location = pw.BooleanField(default=False)
    user = ForeignKeyField(BotUser, backref='store')
    timestamp = pw.DateTimeField(default=datetime.datetime.now)


class Post(BaseModel):
    id = PrimaryKeyField()
    name = pw.CharField(max_length=400)
    desc = pw.TextField()
    price = pw.BigIntegerField()
    brand = pw.CharField(max_length=100)
    category = pw.CharField(max_length=400)
    quick_post = pw.BooleanField(default=False)
    approved = pw.BooleanField(default=False)
    pic = pw.TextField(null=True, default="")
    contact_method = pw.CharField(
        choices=[('phone', 'telegram')], max_length=300, null=True)
    phone = pw.CharField(max_length=300, null=True)
    username = pw.CharField(max_length=300, default="", null=True)
    user = ForeignKeyField(BotUser, backref='user', null=True)
    store = ForeignKeyField(Store, backref='store', null=True)
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
