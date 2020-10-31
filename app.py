from flask import Flask, session

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"  # Don't do this in prod please!

from routes import *

if __name__ == '__main__':
    app.run()