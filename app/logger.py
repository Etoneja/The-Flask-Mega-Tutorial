import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os


def create_logger(app):
    create_file_handler_logger(app)
    # create_smtp_hander_logger(app)


def create_file_handler_logger(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        os.path.join("logs", "microblog.log"),
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


def create_smtp_hander_logger(app):
    if app.debug:
        return
    if not app.config['MAIL_SERVER']:
        return

    auth = None
    if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()
    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'],
        subject='Microblog Failure',
        credentials=auth,
        secure=secure
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
