from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from forms.user import RegisterForm, LoginForm
from data.users import User
from data.films import Films
from data.halls import Hall
from data.sessions import Sessions
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
    sessions_for_films = schedule.remake_shedule()
    db_sess = db_session.create_session()
    result = db_sess.query(Films).all()
    for i in result:
        print(' '.join([j for j in sessions_for_films[i.name]]))
    return render_template('sessions.html', title='Фильмы в прокате сегодня', hire=result, sess=sessions_for_films)
    # f = open("../static/schedule.txt", encoding='windows-1251').read()
    # print(f)


@app.route('/reservation')
def reservation():
    db_sess = db_session.create_session()
    title = request.args.get('title')
    time = request.args.get('time')
    result = db_sess.query(Sessions).filter_by(name=title, time=time).first()
    hall = db_sess.query(Hall).filter_by(id=result.hall).first()
    rows, cols = hall.rows, hall.columns
    seats = [[False for j in range(cols)] for i in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if result.places[i * cols + j] == '1':
                seats[i][j] = True
    return render_template('reservation.html', title=title, time=time, seats=seats, rows=rows, cols=cols)


@app.route('/reservation/buy')
def buy():
    title = request.args.get('title')
    time = request.args.get('time')
    place = request.args.get('place')
    col = request.args.get('col')
    if request.method == 'POST':
        print('Купили место')
    return render_template('buy_seat.html', title=title, time=time, place=place, col=col)


@app.route('/reservation/bought')
def bought():
    title = request.args.get('title')
    time = request.args.get('time')
    place = request.args.get('place')
    col = request.args.get('col')
    print('Купили место ' + place + ' в ряду ' + col)
    return redirect(url_for('.reservation', title=title, time=time))


@app.route('/login', methods=['POST'])
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
