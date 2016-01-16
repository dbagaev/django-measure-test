from .models import models

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from pyxperiment.experiment import Experiment, Registry
from pyxperiment.runner import Runner

import pyxperiment.tests.SimpleTest


# Create your views here.

def index(request):
    out = []

    context = {'tests': models.ExperimentSet.objects.all()}

    return render(request, 'django-pyxperiment/index.html', context)


def test_view(request, test_id):

    exp_set = models.ExperimentSet.objects.filter(Type=test_id)
    if len(exp_set) == 0 :
        raise Http404
    exp_set = exp_set[0]

    context = {
        'test': exp_set,
        'runs': models.ExperimentSetRun.objects.all().prefetch_related()
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

    return render(request, 'django-pyxperiment/run/view.html', context)