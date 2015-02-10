from django.conf.urls import patterns, url
from views import UploadView, CheckStateView


# JSON REQUESTS
urlpatterns = patterns('',
    url(r'^upload/$', UploadView.as_view()),
    url(r'^state/$', CheckStateView.as_view()),
)
