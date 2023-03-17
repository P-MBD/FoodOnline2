from django.urls import path,include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('',AccountViews.vendorDashboard,name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    #path('menu-builder',views.menu_builder,,views.PostListView.as_view()name='menu_builder'),
    path('menu-builder',views.menu_builder.as_view(),name='menu_builder'),
    #path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category.as_view(), name='fooditems_by_category'),

    # Category CRUD
    #path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/add/', views.add_category.as_view(), name='add_category'),
    #path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category.as_view(), name='edit_category'),
    #path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category.as_view(), name='delete_category'),

    #FoodItem CRUD
    path('menu-builer/food/add/',views.add_food.as_view(), name="add_food"),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food.as_view(), name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/',views.delete_food.as_view(),name='delete_food'),

]