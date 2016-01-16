from pyxperiment.experiment import ExperimentSet, Registry
from pyxperiment.runner import Runner
from pyxperiment.metric import Metric

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.views.generic import View

from .models import models

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
            exp_set_res_data = models.ExperimentSetRun(ExperimentSet = set_data, Run = run_data)
            exp_set_res_data.save()

            for m in exp_set_res[1].Metrics.items() :
                metric_data = models.Metric.objects.filter(ExperimentSet=set_data, Name=m[0])
                if len(metric_data) == 0 :
                    raise Exception("Registered metric '" + m[0] + "' not found")
                metric_data = metric_data[0]
                self._saveMetric(m[1], metric_data, run_data, exp_set_res_data)

            for case_res in exp_set_res[1].ExperimentResults.items() :
                # Find appropriate experiment
                exp_data = models.Experiment.objects.filter(ExperimentSet=set_data, Name=case_res[0])

                exp_res_data = models.ExperimentRun(
                        ExperimentSetRun=exp_set_res_data,
                        Experiment = exp_data[0],
                        Run = run_data)
                exp_res_data.save()

                # Save per-experiment metrics
                for m in case_res[1].Metrics.items() :
                    metric_data = models.Metric.objects.filter(ExperimentSet=set_data, Name=m[0])
                    if len(metric_data) == 0 :
                        raise Exception("Registered metric '" + m[0] + "' not found")

                    metric_data = metric_data[0]
                    self._saveMetric(m[1], metric_data, run_data, exp_set_res_data, exp_res_data)

        return redirect(reverse('django-pyxperiment:test.view', kwargs={'test_id' : test_id}))

    def _saveMetric(self, metric, metric_data, run_data, experiment_set_run_data, experiment_run_data = None) :
        if experiment_run_data is not None :
            metric_value_data = models.MetricValue(
                    ExperimentRun=experiment_run_data,
                    ExperimentSetRun=experiment_set_run_data,
                    Run=run_data, Metric=metric_data)
        else :
            metric_value_data = models.MetricValue(
                    ExperimentSetRun=experiment_set_run_data,
                    Run=run_data, Metric=metric_data)
        metric_value_data.save()

        if metric.Type != metric_data.Type :
            raise Exception("Saved metric '" + metric.Name + "' type " + str(metric_data.Type) + " and actual metric type " + str(metric.Type) + " do not match")

        if metric.Type == Metric.TYPE_STRING :
            metric_typed_value_data = models.MetricStringValue(MetricValue=metric_value_data, Value=str(metric.Value))
        elif metric.Type == Metric.TYPE_INTEGER :
            metric_typed_value_data = models.MetricIntegerValue(MetricValue=metric_value_data, Value=int(metric.Value))
        elif metric.Type == Metric.TYPE_FLOAT :
            metric_typed_value_data = models.MetricFloatValue(MetricValue=metric_value_data, Value=float(metric.Value))
        elif metric.Type == Metric.TYPE_BOOLEAN :
            metric_typed_value_data = models.MetricBooleanValue(MetricValue=metric_value_data, Value=bool(metric.Value))
        elif metric.Type == Metric.TYPE_FILE :
            raise Exception("File metric type does not supported yet")
        else :
            raise Exception("Unknown/unsupported metric type " + str(metric.Type) + " for metric " + metric.Name)

        print("saving : " + metric.Name + " = " + str(metric.Value))
        metric_typed_value_data.save()