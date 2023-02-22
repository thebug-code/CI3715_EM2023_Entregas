from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Create the app
app = Flask(__name__)
# Set secret key
app.config['SECRET_KEY'] = '93050512098f85f9bbf0369c3a39c610'
# configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# create the extension
db = SQLAlchemy(app)

from src.login import *

if __name__ == '__main__':
    app.run(debug=True)
