from flask import Flask, redirect, render_template, flash, request, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "hush"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def landing():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if "user" in session:
        return redirect(f'/users/{session["user"]}')
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        new_user = User.register(username=username, password=password,
                                 first_name=first_name, last_name=last_name,
                                 email=email)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors = [
                "Sorry the username '{username}' already exists."]
            return render_template('register.html', form=form)
        session['user'] = new_user.username
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session:
        return redirect(f'/users/{session["user"]}')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data, password=form.password.data)
        if user:
            session['user'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Incorrect username or password"]

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/users/<username>')
def user_display(username):
    if "user" in session:
        user = User.query.get_or_404(username)
        return render_template("user_display.html", user=user)
    return redirect('/')


@app.route('/users/<username>/delete', methods=['POST'])
def user_delete(username):
    if user_check(username):
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.clear()
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(
            title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    return render_template('feedback_form.html', form=form)


@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    if not user_check(feedback.username):
        return redirect('/')
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    return render_template('feedback_form.html', form=form)


@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def feedback_delete(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if user_check(feedback.username):
        db.session.delete(feedback)
        db.session.commit()
    return redirect(f'/users/{feedback.username}')


def user_check(username):
    return session['user'] == username
