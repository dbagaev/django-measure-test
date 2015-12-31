from django.shortcuts import render
from django.http import HttpResponse

from MeasureTest.MeasureTest import *

# Create your views here.

def index(request) :
    out = []

    context = {'tests': []}

    for cls in MeasuredTest.All :
        e = cls()
        e.TestName = e.__class__.__name__
        e.test()

        context['tests'].append(e)

        #members = inspect.getmembers(e)
        #for m in members :
        #    if isinstance(m[1], OutputParameter) :
        #        out.append("Output parameter found: %s = %s" % (e.__class__.__name__ + '.' + m[0], m[1](e)))

    return render(request, 'django-measure-test/index.html', context)
