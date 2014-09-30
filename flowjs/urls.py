from django.conf.urls import patterns, url
from views import UploadView


# JSON REQUESTS
urlpatterns = patterns('',
    url(r'^upload/$', UploadView.as_view()),
)
