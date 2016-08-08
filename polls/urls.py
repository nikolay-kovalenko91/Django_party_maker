from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login', views.login_page, name='login'),
    url(r'^vk', views.vk_handler, name='vk_handler'),
    url(r'^new_poll', views.new_poll, name='new_poll'),
    url(r'^polls_list', views.polls_list, name='polls_list'),
]