from django.urls import path
from . import views, payment_views, player_views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    # path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('player/', player_views.index, name='player'),
    path('payment/', payment_views.index, name='payment'),
]