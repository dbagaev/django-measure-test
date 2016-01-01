from django.shortcuts import render
from django.http import HttpResponse, Http404

from MeasureTest.MeasuredTest import MeasuredTest

import MeasureTest.tests.SimpleTest

# Create your views here.

def index(request) :
    out = []

    context = {'tests': MeasuredTest.All.values() }

    return render(request, 'django-measure-test/index.html', context)

def test_view(request, id) :

    context = {}

    for t in MeasuredTest.All.values() :
        if t.testType() == id :
            context['test'] = t

            cases = t.findTests()
            context['cases'] = cases
            context['metrics'] = t.metrics()

            return render(request, 'django-measure-test/test/view.html', context)

    raise Http404

def test_case_run(request, test_id, case_name) :
    context = {}

    for t in MeasuredTest.All.values() :
        if t.testType() == test_id :
            context['test'] = t

            for case in  t.findTests() :
                if case.name == case_name :
                    context['case'] = case
                    context['metrics'] = t(case)

            return render(request, 'django-measure-test/test/run.html', context)

    raise Http404
