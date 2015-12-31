from django.shortcuts import render
from django.http import HttpResponse

from MeasureTest.MeasureTest import *

# Create your views here.

def index(request) :
    out = []

    for cls in MeasuredTest.All :
        e = cls()
        e.test()

        members = inspect.getmembers(e)
        for m in members :
            if isinstance(m[1], OutputParameter) :
                out.append("Output parameter found: %s = %s" % (m[0], m[1](e)))

    return HttpResponse("<br>".join(out))
