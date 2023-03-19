from django.urls import path
from . import views
urlpatterns=[
    path('',views.MarketPlace.as_view(), name='marketplace'),
]