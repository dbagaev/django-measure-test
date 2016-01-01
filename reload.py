from . import models

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from MeasureTest.MeasuredTest import MeasuredTest


def reload_cases(test, mdl_test):
    for mdl_case in models.TestCase.objects.all():
        case_found = False
        for case in test.findTests():
            if case.name == mdl_case.Name:
                case_found = True
                break

        if not case_found:
            mdl_case.delete()

    for case in test.findTests():
        mdl_case = models.TestCase.objects.filter(Name=case.name, Test=mdl_test)
        if len(mdl_case) == 0:
            mdl_case = models.TestCase(Name=case.name, Test=mdl_test)
            mdl_case.save()


def reload_metrics(test, mdl_test):
    for metric in test.metrics():
        mdl_metric = models.TestMetric.objects.filter(Name=metric.Name, Test=mdl_test)
        if len(mdl_metric) == 0:
            mdl_metric = models.TestMetric(Name=metric.Name, Type=metric.Type, Test=mdl_test)
            mdl_metric.save()


def reload(request):
    for mdl_test in models.Test.objects.all():
        test_registered = False
        for test in MeasuredTest.All.values():
            if test.testType() == mdl_test.Type:
                test_registered = True
                break

        if not test_registered:
            mdl_test.delete()

    for test in MeasuredTest.All.values():
        mdl_test = models.Test.objects.filter(Type=test.testType())
        if len(mdl_test) == 0:
            mdl_test = models.Test(Type=test.testType())
            mdl_test.save()
        else:
            mdl_test = mdl_test[0]

        reload_cases(test, mdl_test)
        reload_metrics(test, mdl_test)

    return redirect('django-measure-test:index')
