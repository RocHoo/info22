from flask import session,render_template,current_app

from . import news_blue

@news_blue.route('/')
def index():
    session['itcast']='2019'
    return render_template('news/index.html')


@news_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')