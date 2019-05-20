from flask import Flask, request, redirect, render_template, session, flash
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

@app.before_request
def require_login():
    allowed_routes = ["login","register","blogs"]
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

#@app.before_request
#def show_blog():


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html',users=users)

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
    return render_template('show-blog.html',blogs=[blog])

@app.route("/user/<int:user_id>")
def get_user_blogs(user_id):
    user_blogs = Blog.query.filter_by(owner_id=user_id).all()
    return render_template('user-blogs.html', blogs=user_blogs)

    

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not_blank(username) and not_blank(password):
            if user and user.password == password:
                session['username'] = username
                flash('Logged in')        
                return redirect('/add-blog')
            else:
                return '<h1>Invalid Information was entered </h1>'
                flash('User password incorrect or user does not exist','error')
        else:
            flash('User password incorrect or user does not exist','error')

    return render_template('/login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blogs')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if password != verify:
            return render_template('register.html')

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/add-blog')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate User</h1>"
    return render_template('/register.html')


@app.route('/blogs', methods=['POST','GET'])
def blogs():
    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs)


if __name__ == '__main__':
    app.run()