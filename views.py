from django.shortcuts import render
from django.http import HttpResponse

from MeasureTest.MeasureTest import *

# Create your views here.

def index(request) :
    out = []

    context = {'tests': MeasuredTest.All.values() }

    return render(request, 'django-measure-test/index.html', context)
