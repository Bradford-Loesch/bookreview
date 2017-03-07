from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^main$', views.main),
    url(r'^books$', views.main),
    url(r'^users/(?P<uid>[0-9]+)$', views.users),
    url(r'^books/add$', views.bookreview),
    url(r'^books/addnow$', views.addbook),
    url(r'^books/addreview$', views.addreview),
    url(r'^books/(?P<bid>[0-9]+)$', views.books),
    url(r'^logout$', views.logout),
    # url(r'^admin/', admin.site.urls),
]
