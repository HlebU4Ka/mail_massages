from django.shortcuts import render, get_object_or_404, redirect
from .models import Newsletter
from .forms import NewsletterForm


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


def newsletter_delete(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.delete()
    return redirect('newsletter_list')
