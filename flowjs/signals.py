import django.dispatch

file_is_ready = django.dispatch.Signal()
file_upload_failed = django.dispatch.Signal()
file_joining_failed = django.dispatch.Signal()