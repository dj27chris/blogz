from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy  
from hashfunc import make_hash_pw, check_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz289o@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column.(db.String(120), unique=True)
    pw_hash = db.Column(db.String(120))
    posts = db.relastionship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.pw_hash = make_hash_pw(password)


@pp.before_request
def requre_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        usernmae = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = Users.query.filter_by(username=username).first()

        if user and check_hash(password, user.pw_hash):
            session['username'] = username
            flash("You are logged in.")
            return redirect('/newpost')
        else:
            flash('Log in user and/or password is incorrect or does not exit', 'error')

        return render_template('login.html')
    
@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        if password != verify:
            return '<h2>Passwords do not match</h2><br><a href="/signup">Go Back</a>'


        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password, email)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            return '<h2> Duplicate user</h2><br><a href="/register">Go Back</a>'
   
    return render_template('signup.html')


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

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/login')



if __name__ == '__main__':
    app.run()