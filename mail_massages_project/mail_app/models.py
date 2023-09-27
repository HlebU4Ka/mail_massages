from django.db import models


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Newsletter(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )

    send_time = models.TimeField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    status = models.CharField(max_length=20, default='created')
    clients = models.ManyToManyField(Client, related_name='newsletters')

    def get_frequency_display(self):
        for frequency, display_name in self.FREQUENCY_CHOICES:
            if frequency == self.frequency:
                return display_name
        return None

    def __str__(self):
        return f"Рассылка ({self.get_frequency_display()})"


class Message(models.Model):
    objects = None
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


class DeliveryLog(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    delivery_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    server_response = models.TextField(blank=True)

    def __str__(self):
        return f"Лог рассылки ({self.delivery_time})"
