from django.core.mail import send_mail
from django.utils import timezone
from mail_app.models import Newsletter, Message, DeliveryLog
import os

def send_newsletters():
    now = timezone.now().time()

    # Получаем рассылки, которые нужно отправить
    newsletters_to_send = Newsletter.objects.filter(
        send_time__lte=now,
        end_time__gte=now,
        status='started'
    )

    for newsletter in newsletters_to_send:
        # Получаем всех клиентов указанных в настройках рассылки
        clients = newsletter.clients.all()

        for client in clients:
            # Отправка сообщений для рассылки
            messages = Message.objects.filter(newsletter=newsletter)

            for message in messages:
                # Логируем попытку отправки
                log = DeliveryLog(
                    newsletter=newsletter,
                    delivery_time=timezone.now(),
                    status='attempted',
                    client=client
                )
                log.save()

                try:
                    send_mail(
                        message.subject,
                        message.body,
                        os.getenv("mail"),  # Замените на реальный отправитель
                        [client.email],  # Отправляем письмо клиенту
                        fail_silently=False,
                    )
                    log.status = 'success'
                except Exception as e:
                    log.status = 'failure'
                    log.server_response = str(e)

                log.save()

        # Помечаем рассылку как завершенную для всех клиентов
        newsletter.status = 'completed'
        newsletter.save()

if __name__ == "__main__":
    send_newsletters()
