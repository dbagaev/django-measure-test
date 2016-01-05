from django.conf.urls import url

from . import views
from . import reload

app_name = 'django-pyxperiment'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reload$', reload.reload, name='reload'),
    url(r'^test/(?P<id>[0-9A-Za-z]+)/view$', views.test_view, name='test.view'),

    url(r'^test/(?P<test_id>[0-9A-Za-z]+)/case/(?P<case_name>[^/]+)/run$', views.test_case_run, name='test.case.run'),
]