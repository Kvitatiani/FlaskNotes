from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, NotesForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secreterium5555'
Bootstrap(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    notes = db.relationship('Note')


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def home():
    return render_template('index.html', user=current_user)


@app.route('/notes', methods=['GET', 'POST'])
@login_required
def add_note():
    form = NotesForm()
    new_note = Note(
        text=form.text.data,
        user_id=current_user.id
    )
    if form.validate_on_submit():
        db.session.add(new_note)
        db.session.commit()
    return render_template('notes.html', form=form, user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(email=email).first()
    if form.validate_on_submit():
        if not user:
            flash("Email doesn't exist, try again.")
        elif not check_password_hash(user.password, password):
            flash('Password is incorrect, try again')
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form, user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(email=email).first()
    if form.validate_on_submit():
        if user:
            flash('User with that email already exists, login instead')
            return redirect(url_for('login'))
        else:
            new_user = User(
                name=form.name.data,
                email=email,
                password=generate_password_hash(
                    password=password, method='sha256', salt_length=8)
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template('register.html', form=form, user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
