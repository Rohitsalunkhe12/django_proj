from django.urls import path
from seller import views

from django.conf import settings
from django.conf.urls.static import static  #Used to serve media files during development

urlpatterns = [
    path('', views.dashboard),
    path('add/', views.app_car),
    path('delete/<car_id>', views.delete_cars),
    path('update/<car_id>', views.update_cars),
    path('cars/', views.view_cars),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


