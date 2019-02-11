from flask import Flask,session

from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager

from flask_migrate import Migrate,MigrateCommand

from flask_session import Session

from config import config_dict

app=Flask(__name__)
app.config.from_object(config_dict('development'))
Session(app)
db=SQLAlchemy(app)
manage=Manager(app)
Migrate(app,db)
manage.add_command('db',MigrateCommand)


@app.route('/')
def index():
    session['itcast']='2019'
    return 'hello world'

if __name__ == '__main__':
    manage.run()