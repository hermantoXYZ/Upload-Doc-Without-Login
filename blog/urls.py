from . import views
from django.urls import path



urlpatterns = [
    path('', views.PostList, name='home'),
    path('list-user/', views.list_user, name='list_user'),


]

