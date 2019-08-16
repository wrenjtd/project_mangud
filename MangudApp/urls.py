from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'MangudApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.mylogout, name='logout'),
    path('members/', views.members, name='members'),
    path('create_user/', views.create_user, name='create_user'),
    path('create_user_submission/', views.create_user_submission, name='create_user_submission'),
    path('members/edit_user_submission/', views.edit_user_submission, name='edit_user_submission'),
    path('members/change_password_submission/', views.change_password_submission, name='change_password_submission'),
    path('verify_user/', views.verify_user, name='verify_user'),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('<int:games_id>/', views.game_details, name='a_game'),
]