from flask import Flask,session

from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager

from flask_migrate import Migrate,MigrateCommand

from flask_session import Session

from redis import StrictRedis
app=Flask(__name__)
app.config['SECRET_KEY']='pr2fPX72RfUAMJEMA+u7pUILxC9CYcjFUY9JiPjA3111hKkETyZiYw=='
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=StrictRedis(host='127.0.0.1',port=6379)
app.config['SESSION_USE_SINGER']=True
app.config['PERMANENT_SESSION_LIFETIME']=86400
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:mysql@localhost/info22'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
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