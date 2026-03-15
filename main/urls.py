from django.urls import path
from . import views

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('tours/', views.tour_list, name='tour_list'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('booking/', views.booking_view, name='booking'),
]