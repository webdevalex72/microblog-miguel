import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask import request


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
# Important - next string have to write after 'app.config.from_object(Config)'
mail = Mail(app)
babel = Babel(app) 

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


from app import routes, models, errors
"""
Сценарий выше просто создает объект приложения как экземпляр класса Flask,
импортированного из пакета flask. Переменная __name__, переданная в класс
Flask, является предопределенной переменной Python, которая задается именем
модуля, в котором она используется. Flask использует расположение модуля,
переданного здесь как отправную точку, когда ему необходимо загрузить
связанные ресурсы, такие как файлы шаблонов, которые я расскажу в главе 2.
Для всех практических целей передача __name__ почти всегда будет настраивать
flask в правильном направлении. Затем приложение импортирует модуль routes,
который еще не существует.
....
..модуль routes импортируется внизу, а не наверху скрипта, как это всегда
делается.
Нижний импорт является обходным путем для циклического импорта, что является
общей проблемой при использовании приложений Flask. Вы увидите, что модуль
routes должен импортировать переменную приложения, определенную в этом скрипте,
поэтому, поместив один из взаимных импортов внизу, вы избежите ошибки,
которая возникает из взаимных ссылок между этими двумя файлами.
"""
