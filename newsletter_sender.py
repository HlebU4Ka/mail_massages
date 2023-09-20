import os
import sys
import django

# Скрипт для рассылки
# Указываем путь к файлу settings.py для Django
sys.path.append('mail_massages_project/mail_app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mail_app.settings'

# Инициализация Django
django.setup()

from django.core.mail import send_mail
from django.utils import timezone
from mail_app import Newsletter, Message, DeliveryLog


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
                    message.body,
                    # 'от_кого@example.com',
                    # ['куда@example.com'],  # Замените на адрес получателя
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
