from django.conf.urls import url

from . import views
from . import reload
from . import run

app_name = 'django-pyxperiment'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reload$', reload.reload, name='reload'),
    url(r'^test/(?P<test_id>[0-9A-Za-z]+)/view$', views.test_view, name='test.view'),

    url(r'^test/(?P<test_id>[0-9A-Za-z]+)/case/(?P<case_name>[^/]+)/run$', views.test_case_run, name='test.case.run'),

    url(r'^test/(?P<test_id>[0-9A-Za-z]+)/run$', run.Run.as_view(), name='test.run'),

    url(r'^run/(?P<run_id>[0-9]+)/view$', views.run_view, name='run.view'),

    url(r'^test/(?P<test_id>[0-9A-Za-z]+)/values', views.get_values, name='test.values'),
    #url(r'^test/(?P<test_id>[0-9A-Za-z]+)/case/(?P<case_id>[0-9]+)/values', views.get_values, name='test.case.values')

]