# send_newsletters.py

import os
import sys
import django

# Указываем путь к файлу settings.py для Django
sys.path.append('D:/pythonProject/mail_massages/mail_massages_project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mail_massages_project.settings'

# Инициализация Django
django.setup()

from django.core.mail import send_mail
from django.utils import timezone
from mail_app.models import Newsletter, Message, DeliveryLog

def send_newsletters():
    # Отправка рассылок
    now = timezone.now()

    # Получаем рассылки, которые нужно отправить
    newsletters_to_send = Newsletter.objects.filter(send_time__lte=now, status='created')

    for newsletter in newsletters_to_send:
        # Отправка сообщений для рассылки
        messages = Message.objects.filter(newsletter=newsletter)
        for message in messages:
            # Логируем попытку отправки
            log = DeliveryLog(
                newsletter=newsletter,
                delivery_time=now,
                status='attempted'
            )
            log.save()

            # Отправляем сообщение
            try:
                send_mail(
                    message.subject,
                    message.content,
                    'от_кого@example.com',  # Замените на реальный отправитель
                    [message.recipient_email], # Замените на реальный получатель
                    fail_silently=False,
                )
                log.status = 'success'
            except Exception as e:
                log.status = 'failure'
                log.server_response = str(e)

            log.save()

            # Помечаем рассылку как завершенную
            newsletter.status = 'completed'
            newsletter.save()

if __name__ == "__main__":
    send_newsletters()
