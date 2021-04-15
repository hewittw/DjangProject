from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stream', views.stream, name='stream'),
    path('thread/<int:pId>', views.thread, name='thread'),
    path('profile/<int:profileId>', views.profile, name='profile'),
]
