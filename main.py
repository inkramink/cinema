from flask import Flask, render_template, redirect

from data.users import User
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    #db_session.global_init("db/blogs.db")
    app.run()


@app.route("/")
def index():
    #db_sess = db_session.create_session()
    return render_template("base.html")


if __name__ == '__main__':
    main()
