from django.template.loader import render_to_string
from django.core.signing import Signer
from datetime import datetime
from os.path import splitext

from bboard.settings import ALLOWED_HOSTS

signer = Signer()


def send_activation_notification(user):
    """Отправляем письмо"""
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]

    else:
        host = 'http://127.0.0.1:8000'
    context = {'user': user, 'host': host,
               'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt',
                               context)
    body_text = render_to_string('email/activation_letter_body.txt',
                                 context)
    user.email_user(subject, body_text)


def get_timestamp_path(instance, filename):
    """Генерирует имена сохраняемых в модели выгруженных файлов"""
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])


def send_new_comment_notification(comment):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://127.0.0.1:8000'
    author = comment.bb.author
    context = {'author': author, 'host': host, 'comment': comment}
    subject = render_to_string('email/new_comment_latter_subject.txt', context)
    body_text = render_to_string('email/new_comment_latter_body.txt', context)
    author.email_user(subject, body_text)