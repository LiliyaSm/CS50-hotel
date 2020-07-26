from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("booking", views.BookingView.as_view(), name="booking"),
    path('rooms', views.CategoryListView.as_view(), name='rooms'),
    path('rooms/<slug:name>', views.CategoryDetail.as_view(), name='room-detail'),
    path('booking_submit', views.booking_submit, name='booking_submit'),
    path('confirm', views.ConfirmView.as_view(), name='confirm'),]
    
# urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
