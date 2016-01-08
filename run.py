from pyxperiment.registry import Registry
from pyxperiment.experiment import ExperimentSet
from pyxperiment.runner import Runner
from pyxperiment.metric import Metric

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.views.generic import View

from . import models

class Run(View) :
    def get(self, request, test_id = None) :
        # first find test set to run
        exp_set = Registry.get(test_id)
        if exp_set is None :
            raise Http404

        runner = Runner()
        runner.add(exp_set)
        result = runner.run()

        # Now let's save all data into database
        run_data = models.Run()
        run_data.save()
        for exp_set_res in result.SetResults.items() :
            set_data = models.ExperimentSet.objects.filter(Type=exp_set_res[0])
            if len(set_data) == 0 :
                raise Exception("Registered experiment set '" + exp_set_res[0] + "' not found")
            set_data = set_data[0]
            # Save set-vise metrics
            for m in exp_set_res[1].Metrics :
                metric_data = models.Metric.objects.filter(ExperimentSet=set_data, Name=m[0])
                if len(metric_data) == 0 :
                    raise Exception("Registered metric '" + m[0] + "' not found")
                metric_data = metric_data[0]
                self._saveMetric(m[1], metric_data, run_data)

            for case_res in exp_set_res[1].ExperimentResults.items() :
                # Find appropriate experiment
                exp_data = models.Experiment.objects.filter(ExperimentSet=set_data, Name=case_res[0])

                exp_res_data = models.ExperimentRun()
                exp_res_data.Experiment = exp_data[0]
                exp_res_data.Run = run_data
                exp_res_data.Success = 0
                exp_res_data.save()

                # Save per-experiment metrics
                for m in case_res[1].Metrics :
                    metric_data = models.Metric.objects.filter(ExperimentSet=set_data, Name=m[0])
                    if len(metric_data) == 0 :
                        raise Exception("Registered metric '" + m[0] + "' not found")

                    metric_data = metric_data[0]
                    self._saveMetric(m[1], metric_data, run_data)

        return redirect(reverse('django-pyxperiment:test.view', kwargs={'test_id' : test_id}))

    def _saveMetric(self, metric, metric_data, run_data, experiment_run_data = None) :
        if experiment_run_data is not None :
            metric_value_data = models.MetricValue(ExperimentRun=experiment_run_data, Run=run_data, Metric=metric_data)
        else :
            metric_value_data = models.MetricValue(Run=run_data, Metric=metric_data)
        metric_value_data.save()

        if metric.Type != metric_data.Type :
            raise Exception("Saved metric '" + metric.Name + "' type " + str(metric_data.Type) + " and actual metric type " + str(metric.Type) + " do not match")

        if metric.Type == Metric.TYPE_STRING :
            metric_typed_value_data = models.MetricStringValue(MetricValue=metric_value_data, Value=str(metric()))
        elif metric.Type == Metric.TYPE_INTEGER :
            metric_typed_value_data = models.MetricIntegerValue(MetricValue=metric_value_data, Value=int(metric()))
        elif metric.Type == Metric.TYPE_FLOAT :
            metric_typed_value_data = models.MetricFloatValue(MetricValue=metric_value_data, Value=float(metric()))
        elif metric.Type == Metric.TYPE_BOOLEAN :
            metric_typed_value_data = models.MetricBooleanValue(MetricValue=metric_value_data, Value=bool(metric()))
        elif metric.Type == Metric.TYPE_FILE :
            raise Exception("File metric type does not supported yet")
        else :
            raise Exception("Unknown/unsupported metric type " + str(metric.Type) + " for metric " + metric.Name)

        metric_typed_value_data.save()