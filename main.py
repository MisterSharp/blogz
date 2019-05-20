from flask import Flask, request, redirect, render_template,session, flash
from flask_sqlalchemy import SQLAlchemy
from helpers import len_check, not_blank

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:codecamp2019@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "ienzbxotzq"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogz = db.relationship('Blog', backref='owner')

    def __init__(self, username, password,):
        self.username = username
        self.password = password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-blog', methods=['POST', 'GET'])
def add_blog():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        if not_blank(blog_title) and not_blank(blog_body):
            new_blog = Blog(blog_title, blog_body,owner)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog/'+ str(new_blog.id))
        else:
            return render_template('add-blog.html')
    else:
        return render_template('add-blog.html')
    

@app.route("/blog/<int:blog_id>")
def get_blog(blog_id):
    blog = Blog.query.get(blog_id)
    return render_template('index.html',blogs=[blog])

    

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        #TODO if login is successfull
            #route to /add-blog
        pass
    return render_template('/login')

@app.route('/blogs', methods=['POST'])
def posted():
    blogs = Blog.query.all()
    return render_template('index.html', blogs=blogs)


if __name__ == '__main__':
    app.run()