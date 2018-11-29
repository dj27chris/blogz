from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy  

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz289o@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body




@app.route('/', methods=['POST', 'GET'])
def index():

    posts = Blog.query.all()

    return render_template('blog.html', title="Blog", posts=posts)


@app.route('/post/<int:post_id>', methods=['GET'])
def post(post_id):

    post = Blog.query.get(post_id)

    return render_template('blog.html', title="Blog", posts=[post])

@app.route('/newpost', methods=['GET'])
def newpost():

    return render_template('newpost.html', title="Add a Post")


@app.route('/addpost', methods=['POST'])
def addpost():
    new_title = request.form['title']
    new_body = request.form['body']
    new_post = Blog(new_title, new_body)
    db.session.add(new_post)
    db.session.commit()

    return redirect('/')


    



if __name__ == '__main__':
    app.run()