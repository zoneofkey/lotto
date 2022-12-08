from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('main_l', views.main_l, name="main_l"),
    path('main_l/<int:pk>', views.posting, name="posting"),
    path('new_post', views.new_post, name='new_post'),
    path('main_l/<int:pk>/remove', views.remove_post, name='remove_post'),
    path('lotto_main', views.lotto_main, name='lotto_main'),
    path('l_list', views.l_list, name="l_list"),
    path('l_detail/<int:pk>', views.l_detail, name="l_detail"),
    path('l_save', views.l_save, name="l_save"),
    path('l_list_ser', views.l_list_ser, name="l_list_ser"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)