import os
from flask import Flask
from flask import render_template, redirect, url_for
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
from data.theses import Theses
from forms.user import LoginForm, RegisterForm
from forms.thesis import ThesesForm
from data import db_session, theses_resources

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/files/'  # Папка для сохранения файлов
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


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
                               form=form, brand_logo=url_for('static', filename='img/IOPS_logo_small.png'))
    return render_template('login.html', title='Авторизация', form=form,
                           brand_logo=url_for('static', filename='img/IOPS_logo_small.png'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   brand_logo=url_for('static', filename='img/IOPS_logo_small.png'))
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   brand_logo=url_for('static', filename='img/IOPS_logo_small.png'))
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            middle_name=form.middle_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            academic_degree=form.academic_degree.data,
            academic_title=form.academic_title.data,
            position=form.position.data,
            organisation=form.organisation.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form,
                           brand_logo=url_for('static', filename='img/IOPS_logo_small.png'))


@app.route('/thesis', methods=['GET', 'POST'])
@login_required
def thesis():
    form = ThesesForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        theses = Theses()
        theses.title = form.title.data
        theses.thesis_filename = form.thesis.data.filename
        theses.user_id = current_user.id
        theses.user = current_user
        file = form.thesis.data
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        current_user.thesis = [theses]
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('theses.html', title='Добавление тезисов',
                           form=form, brand_logo=url_for('static', filename='img/IOPS_logo_small.png'))


@app.route('/dates')
def dates():
    with open('static/info/dates_info.txt', 'r', encoding='utf8') as f:
        return render_template('dates.html', title='Даты проведения', information=f.read(),
                               brand_logo=url_for('static', filename='img/IOPS_logo_small.png'))


#     25.02.2026 23-27


@app.route('/test')
def test():
    db_sess = db_session.create_session()
    users = db_sess.query(User).first()
    return users.__repr__()


@app.route('/')
def index():
    with open('static/info/index_info.txt', 'r', encoding='utf8') as f:
        return render_template('index.html', brand_logo=url_for('static', filename='img/IOPS_logo_small.png'),
                               information=f.read(), title='Главная страница')


def main():
    db_session.global_init('db/conference.db')
    # для списка объектов
    api.add_resource(theses_resources.ThesesListResource, '/api/theses')

    # для одного объекта
    api.add_resource(theses_resources.ThesesResource, '/api/theses/<int:theses_id>')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
