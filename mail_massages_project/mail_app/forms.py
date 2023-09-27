from django import forms
from .models import Client, Newsletter, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['send_time', 'frequency', 'status']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['newsletter', 'subject', 'body']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
