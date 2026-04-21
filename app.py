from flask import Flask, render_template, request, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, UserMixin, logout_user, current_user, login_user
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
SECRET_KEY="This_is_my_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

uri = "postgresql://database_aman:aKYoDNKNv3yGX7ZjLwRrDlhppO8gq85A@dpg-d7ir9on7f7vs739d1ci0-a.oregon-postgres.render.com:5432/friendsdb_v60c"

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    reviews = db.relationship('Review', backref='author', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match"

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return redirect("/login")
            

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=username, password=hashed)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect('/dashboard')

    return render_template('signup.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/dashboard')
        
        return "Invalid Username or Password"

    return render_template('login.html')


@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():

    reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.id.desc()).all()

    return render_template("dashboard.html", reviews=reviews)

@app.route('/add_review', methods=['POST'])
@login_required
def add_review():
    content = request.form.get('review')

    if not content:
        return "Review cannot be empty"

    review = Review(content=content, user_id=current_user.id)
    db.session.add(review)
    db.session.commit()

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0",port= 5432)

