from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'MAIN PAGE'

@app.route('/about')
def about():
    return 'THIS IS THE ABOUT PAGE'

@app.route('/blog')
def blog():
    return 'HERE WILL BE ARTICLES'
