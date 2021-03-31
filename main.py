from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from forms.user import RegisterForm, LoginForm
from data.users import User
from data.films import Films
from data import schedule
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/cinema.db")
    app.run()


@app.route('/', methods=['GET'])
def index():
    db_sess = db_session.create_session()
    return render_template("main_page.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/hire')
def hire():
    db_sess = db_session.create_session()
    result = db_sess.query(Films).all()
    return render_template('hire.html', title='Aфиша', hire=result)


@app.route('/sessions')
def sessions():
    db_sess = db_session.create_session()
    result = db_sess.query(Films).all()
    sessions_for_films = schedule.remake_shedule()
    return render_template('sessions.html', title='Фильмы в прокате сегодня', hire=result, sess=sessions_for_films)
    # f = open("../static/schedule.txt", encoding='windows-1251').read()
    # print(f)


@app.route('/reservation')
def reservation():
    title = request.args.get('title')
    time = request.args.get('time')
    return render_template('reservation.html', title=title, time=time)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
    """
    db_sess = db_session.create_session()
    result = db_sess.query(User).all()
    for us in result:
        print(us.name)
    
    """
