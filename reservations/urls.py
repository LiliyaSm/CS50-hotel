from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("cart", views.cart, name="cart"),
    # path('add_to_cart/', views.add_to_cart, name='add_to_cart'), 
    # path('delete_item/', views.delete_item, name='delete_item'),
    # path('update_cart/', views.update_cart, name='update_cart'), 
    # path('confirm_cart/', views.confirm_cart, name='confirm_cart'), 
    # path('order_history/', views.order_history, name='order_history'), 
    # path('cart/<int:id>/', views.order_detail, name='order_detail'), 
    # path('cart/<int:id>/repeat', views.order_repeat,
    #      name ="order_repeat")  
]