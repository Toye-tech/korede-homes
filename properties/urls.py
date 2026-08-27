from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='list'),
    path('<slug:slug>/', views.property_detail, name='detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)