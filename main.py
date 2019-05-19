from flask import Flask, request, redirect, render_template,session, flash
from flask_sqlalchemy import SQLAlchemy
from helpers import len_check, not_blank

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:codecamp2019@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "ienzbxotzq"

class User(db.Model)
    id = db.Column(db.Integer, primary_key=True)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('index.html', blogs=blogs)

@app.route('/add-blog', methods=['POST', 'GET'])
def add_blog():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        if not_blank(blog_title) and not_blank(blog_body):
            new_blog = Blog(blog_title, blog_body)
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

    

@app.route('/delete-blog', methods=['POST'])
def delete_blog():

    return redirect('/')

@app.route('/posted', methods=['POST'])
def posted():
   return '<h1>Blog Posted</h1>'


if __name__ == '__main__':
    app.run()