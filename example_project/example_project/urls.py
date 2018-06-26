try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


from .views import BasicFormView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    re_path(r'^$', BasicFormView.as_view(), name='form'),
]
