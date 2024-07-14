from django.urls import include, path
from rest_framework import routers
from . import views, payment_views, player_views

router = routers.DefaultRouter()
router.register(r'payment', payment_views.PaymentViewSet)

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    # path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('player/', player_views.index, name='player'),
    path('payment/', payment_views.index, name='payment'),

    path('api/', include(router.urls)),
    # path("api/auth/", include('rest_framework.urls', namespace='rest_framework')),
]