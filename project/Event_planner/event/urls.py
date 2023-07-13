from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('login', views.index2),
    path('register', views.register),
    path('welcome', views.success),
    path('logout', views.logout),
    path('login_vald', views.login),
    path('new_event', views.new),
    path('create', views.create),
    path('view/<int:id>', views.view),
    path('<int:id>/edit', views.edit),
    path('update/<int:id>', views.update),
    path('<int:id>/delete', views.delete)
]