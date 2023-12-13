from django.conf.urls import url, include
from . import views

app_name = 'homepage'

urlpatterns = [
    url(r'^$', views.login_view, name="login"),
    url(r'^options/$', views.options_view, name="options")
   
]
