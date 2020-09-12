from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('generate/pdf/', views.generate_pdf, name='generate_pdf'),
]