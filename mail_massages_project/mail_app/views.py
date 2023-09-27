from .forms import NewsletterForm, MessageForm
from django.shortcuts import get_object_or_404, redirect, render
from .models import Newsletter, Message
import requests


def newsletter_list(request):
    newsletters = Newsletter.objects.all()
    return render(request, 'newsletter_list.html', {'newsletters': newsletters})


def newsletter_detail(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, 'newsletter_detail.html', {'newsletter': newsletter})


def newsletter_new(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.save()
            return redirect('newsletter_detail', pk=newsletter.pk)
    else:
        form = NewsletterForm()
    return render(request, 'newsletter_edit.html', {'form': form})


def newsletter_edit(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.save()
            return redirect('newsletter_detail', pk=newsletter.pk)
    else:
        form = NewsletterForm(instance=newsletter)
    return render(request, 'newsletter_edit.html', {'form': form})


def newsletter_delete(pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.delete()
    return redirect('newsletter_list')


# CRUD

def create_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_message')  #
    else:
        form = MessageForm()
    return render(request, 'create_message.html', {'form': form})


def edit_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('edit_message', message_id=message_id)
    else:
        form = MessageForm(instance=message)
    return render(request, 'edit_message.html', {'form': form})


def delete_messages(message_id):
    message = get_object_or_404(Message, pk=message_id)
    newsletter_id = message.newsletter.id
    message.delete()
    return redirect('newsletter_detail', pk=newsletter_id)


def edit_messages(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    newsletter_id = message.newsletter.id
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('newsletter_detail', pk=newsletter_id)
    else:
        form = MessageForm(instance=message)
    return render(request, 'edit_message.html', {'form': form, 'message': message})


def deleted_messages(message_id):
    message = get_object_or_404(Message, pk=message_id)
    newsletter_id = message.newsletter.id
    message.delete()
    return redirect('newsletter_detail', pk=newsletter_id)


def subscribe_newsletter():
    return None