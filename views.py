from .models import models

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse

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

def get_values(request, test_id, case_id = None) :
    response = {
        'data': None,
        'result': 0
    }
    try :
        exp_set = models.ExperimentSet.findByName(test_id)
        if exp_set is None :
            raise Exception("Cannot find test '%s'" % test_id)

        data = []

        runs = models.ExperimentSetRun.objects.filter(ExperimentSet=exp_set)
        for run in runs :
            run_data = {
                'label': run.Started,
                'values': {}
            }
            for val in run.Values :
                run_data['values'][val.Metric.Name] = val.Value

            data.append(run_data)

        response['data'] = data


    except Exception as e :
        response['result'] = 1
        response['message'] = str(e)

    return JsonResponse(response)
