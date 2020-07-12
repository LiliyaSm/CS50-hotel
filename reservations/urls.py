from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.index, name="index"),
    path("booking", views.booking, name="booking"),
    path('rooms', views.rooms, name='rooms'),
    
     
    # path('delete_item/', views.delete_item, name='delete_item'),
    # path('update_cart/', views.update_cart, name='update_cart'), 
    # path('confirm_cart/', views.confirm_cart, name='confirm_cart'), 
    # path('order_history/', views.order_history, name='order_history'), 
    # path('cart/<int:id>/', views.order_detail, name='order_detail'), 
    # path('cart/<int:id>/repeat', views.order_repeat,
    #      name ="order_repeat")  
]

# urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
