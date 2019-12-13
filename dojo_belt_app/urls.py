from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register_verify', views.register_verify),
    path('login_verify', views.login_verify),
    path('logout', views.logout),
    path('wishes', views.wishes),
    path('wishes/stats', views.user_stats),
    path('wishes/like/<int:id>', views.like),
    path('wishes/new', views.wish_new),
    path('wishes/granted/<int:id>', views.wish_granted),
    path('wishes/new/verify', views.wish_new_verify),
    path('wishes/remove/<int:id>', views.wish_remove),
    path('wishes/edit/<int:id>', views.wish_edit),
    path('wishes/edit/<int:id>/verify', views.wish_edit_verify),
]
