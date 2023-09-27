import os
from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail
from django.utils import timezone
from .models import Newsletter, Message, DeliveryLog


def do():

    now = timezone.now()
    newsletters_to_send = Newsletter.objects.filter(send_time__lte=now, status='created')

    for newsletter in newsletters_to_send:
        messages = Message.objects.filter(newsletter=newsletter)
        for message in messages:
            log = DeliveryLog(
                newsletter=newsletter,
                delivery_time=now,
                status='attempted'
            )
            log.save()

            try:
                send_mail(
                    message.subject,
                    message.content,
                    os.getenv("mail"),  # Замените на реальный отправитель
                    os.getenv("mail_send"),  # Замените на реальный получатель
                    fail_silently=False,
                )
                log.status = 'success'
            except Exception as e:
                log.status = 'failure'
                log.server_response = str(e)

            log.save()

            newsletter.status = 'completed'
            newsletter.save()


class SendNewslettersCronJob(CronJobBase):
    RUN_AT_TIMES = ['01:00', '12:00']  # Время запуска задачи
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
