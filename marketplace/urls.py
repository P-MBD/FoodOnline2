from django.urls import path
from . import views
urlpatterns=[
    path('',views.MarketPlace.as_view(), name='marketplace'),
    path('<slug:vendor_slug>/',views.VendorDetail.as_view(), name="vendor_detail"),
  # ADD TO CART
    #path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
     path('add_to_cart/<int:food_id>/', views.AddToCart.as_view(), name='add_to_cart'),
     #Decrease To CARt
     path('decrease_cart/<int:food_id>/',views.DecreaseCart.as_view(), name='decrease_cart'),

   
    
]