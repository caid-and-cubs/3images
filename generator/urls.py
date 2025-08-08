from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_image, name='generate_image'),
    path('gallery/', views.gallery, name='gallery'),
    path('download/<int:image_id>/', views.download_image, name='download_image'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
]