from django.urls import path

from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('main',views.main,name='main'),
    path('uploads',views.upload,name='upload')
]