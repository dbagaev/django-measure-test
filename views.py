from . import models

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from pyxperiment.experiment import Experiment
from pyxperiment.runner import Runner
from pyxperiment.registry import Registry

import pyxperiment.tests.SimpleTest


# Create your views here.

def index(request):
    out = []

    context = {'tests': models.ExperimentSet.objects.all()}

    return render(request, 'django-pyxperiment/index.html', context)


def test_view(request, test_id):

    test = models.ExperimentSet.objects.filter(Type=test_id)
    if len(test) == 0 :
        raise Http404

    context = {
        'test': test[0],
        'runs': models.Run.objects.all()
    }

    return render(request, 'django-pyxperiment/test/view.html', context)

    raise Http404


def test_case_run(request, test_id, case_name):
    context = {}

    for t in Registry._ExperimentSets.values():
        if t.name == test_id:
            context['test'] = t

            for case in t.findTests():
                if case.name == case_name:
                    context['case'] = case
                    context['metrics'] = t(case)

            return render(request, 'django-pyxperiment/test/run.html', context)

    raise Http404

def run_view(request, run_id) :
    context = {}

    run = models.Run.objects.filter(pk=run_id)

    if len(run) == 0 :
        raise Http404

    run = run[0]

    context['run'] = run
    context['metrics'] = models.MetricValue.objects.filter(Run=run, ExperimentRun=None)

    return render(request, 'django-pyxperiment/run/view.html', context)