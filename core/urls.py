from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service-detail'),
    path('faq/', views.faq, name='faq'),
    path('health/', views.health_check, name='health_check'),
]