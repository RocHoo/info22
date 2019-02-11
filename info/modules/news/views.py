from flask import session

from . import news_blue

@news_blue.route('/')
def index():
    session['itcast']='2019'
    return 'hello world'