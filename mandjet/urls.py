from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('planning/', views.planning, name='planning'),
    path('production/', views.production, name='production'),
    path('book/', views.book_vehicle, name='book'),
   
]