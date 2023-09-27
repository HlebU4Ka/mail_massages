"""
URL configuration for mail_massages_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from mail_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.newsletter_list, name='newsletter_list'),
    path('newsletter/<int:pk>/', views.newsletter_detail, name='newsletter_detail'),
    path('newsletter/new/', views.newsletter_new, name='newsletter_new'),
    path('newsletter/<int:pk>/edit/', views.newsletter_edit, name='newsletter_edit'),
    path('newsletter/<int:pk>/delete/', views.newsletter_delete, name='newsletter_delete'),
    path('create_message/', views.create_message, name='create_message'),
    path('edit_message/<int:message_id>/', views.edit_message, name='edit_message'),
    path('subscribe_newsletter/<int:newsletter_id>/<int:client_id>/', views.subscribe_newsletter, name='subscribe_newsletter'),
]
