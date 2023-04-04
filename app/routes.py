from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Joey'}
    posts = [
        {
            'author' : {'username': 'Joey'},
            'title' : 'CSP',
            'body' : 'This card is great!'
        },
        {
            'author' : {'username': 'Joey'},
            'title' : 'CFU',
            'body' : 'This card is versatile!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
