from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from alice import say
from data import db_session
from forms.user import RegisterForm, LoginForm
from forms.write_comment import ReviewForm
from data.users import User, Anonymous
from data.films import Films
from data.halls import Hall
from data.review import Review
from data.sessions import Sessions
from data import schedule
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous


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


@app.route('/film-info', methods=['GET', 'POST'])
def film_info():
    form = ReviewForm()
    db_sess = db_session.create_session()
    film_id = request.args.get('id')
    if form.comment.data:
        rev = Review(name=current_user.name,
                     date=str(date.today()),
                     comment=form.comment.data,
                     film_id=film_id)
        db_sess.add(rev)
        db_sess.commit()
        return redirect(url_for('.film_info', id=film_id))
    reviews = db_sess.query(Review).filter_by(film_id=film_id).all()
    result = db_sess.query(Films).all()[int(film_id) - 1]
    return render_template('film_info.html', result=result, reviews=reviews, form=form)


@app.route('/sessions')
def sessions():
    sessions_for_films = schedule.remake_shedule()
    db_sess = db_session.create_session()
    result = db_sess.query(Films).all()
    return render_template('sessions.html', title='Фильмы в прокате сегодня', hire=result, sess=sessions_for_films)
    # f = open("../static/schedule.txt", encoding='windows-1251').read()
    # print(f)


@app.route('/reservation')
def reservation():
    db_sess = db_session.create_session()
    title = request.args.get('title')
    time = request.args.get('time')
    hall = request.args.get('hall')
    result = db_sess.query(Sessions).filter_by(name=title, time=time, hall=int(hall)).first()
    find_hall = db_sess.query(Hall).filter_by(id=int(hall)).first()
    rows, cols = find_hall.rows, find_hall.columns
    seats = [[False for j in range(cols)] for i in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if result.places[i * cols + j] == '1':
                seats[i][j] = True
    return render_template('reservation.html', title=title, time=time,
                           hall=hall, seats=seats, rows=rows, cols=cols)


@app.route('/reservation/buy')
def buy():
    title = request.args.get('title')
    time = request.args.get('time')
    hall = request.args.get('hall')
    place = request.args.get('place')
    col = request.args.get('col')
    logged = False
    if current_user.is_authenticated:
        logged = True
    return render_template('buy_seat.html', title=title, time=time,
                           hall=hall, place=place, col=col, logged=logged)


@app.route('/reservation/bought')
def bought():
    title = request.args.get('title')
    time = request.args.get('time')
    hall = request.args.get('hall')
    place = request.args.get('place')
    col = request.args.get('col')
    db_sess = db_session.create_session()
    result = db_sess.query(Sessions).filter_by(name=title, time=time, hall=int(hall)).first()
    sess_id = result.id
    find_hall = db_sess.query(Hall).filter_by(id=int(hall)).first()
    rows, cols = find_hall.rows, find_hall.columns
    seats = list(result.places)
    seats[(int(col) - 1) * int(cols) + int(place) - 1] = '1'
    seats = ''.join(seats)
    db_sess.query(Sessions).filter_by(id=sess_id).update({Sessions.places: seats}, synchronize_session=False)
    db_sess.commit()
    say('Вы купили место ' + place + ' в ряду ' + col +
        ' на сеанс ' + title + ' в ' + time +
        ' в зале номер ' + str(int(find_hall.id) + 1) + ' стоимостью 0 рублей')
    return redirect(url_for('.reservation', title=title, time=time, hall=hall))


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
