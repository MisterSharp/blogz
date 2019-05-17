from flask import Flask, request, redirect, render_template,session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:codecamp2019@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "ienzbxotzq"


@app.route('/')
def index():
    return render_template('base.html')



if __name__ == '__main__':
    app.run()