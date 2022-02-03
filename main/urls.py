
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main_view'),
    path('splash/', views.splash_view, name='splash_view'),
    path('new_listing/', views.new_listing_view, name='new_listing_view'),
    path('your_biddings/', views.your_biddings_view, name='your_biddings_view'),
    path('your_listings/', views.your_listings_view, name='your_listings_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('delete/', views.delete_exchange_view, name='delete_exchange_view'),
]
