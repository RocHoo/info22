from flask import session,render_template

from . import news_blue

@news_blue.route('/')
def index():
    session['itcast']='2019'
    return render_template('news/index.html')