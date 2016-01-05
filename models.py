from django.db import models

from pyxperiment.metric import Metric as exp_Metric

# Create your models here.
class ExperimentSet(models.Model):
    id = models.IntegerField(primary_key=True)
    Type = models.CharField(max_length=128)

    def Experiments(self):
        return Experiment.objects.filter(ExperimentSet=self)

    def Metrics(self):
        return Metric.objects.filter(ExperimentSet=self)


class Experiment(models.Model):
    id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=256)
    ExperimentSet = models.ForeignKey('ExperimentSet', on_delete=models.CASCADE)

    def Metrics(self):
        return Metric.objects.filter(Experiment=self)


class Run(models.Model):
    id = models.IntegerField(primary_key=True)
    Started = models.TimeField()


class ExperimentRun(models.Model):
    id = models.IntegerField(primary_key=True)
    Started = models.TimeField()
    Success = models.IntegerField()
    Run = models.ForeignKey('Run', on_delete=models.CASCADE)
    Experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE)


class Metric(models.Model):
    VALUE_TYPES = (
        (exp_Metric.TYPE_FLOAT, 'Float'),
        (exp_Metric.TYPE_INTEGER, 'Integer'),
        (exp_Metric.TYPE_BOOLEAN, 'Boolean'),
        (exp_Metric.TYPE_STRING, 'String'),
        (exp_Metric.TYPE_FILE, 'File')
    )
    id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=64)
    Type = models.IntegerField(choices=VALUE_TYPES)

    ExperimentSet = models.ForeignKey('ExperimentSet', on_delete=models.CASCADE)

class MetricValue(models.Model):
    id = models.IntegerField(primary_key=True)
    ExperimentRun = models.ForeignKey('ExperimentRun', on_delete=models.CASCADE)
    Run = models.ForeignKey('Run', on_delete=models.CASCADE)
    Metric = models.ForeignKey('Metric', on_delete=models.CASCADE)

class MetricStringValue(models.Model):
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.CharField(max_length=256)


class MetricFloatValue(models.Model):
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.FloatField()


class MetricIntegerValue(models.Model):
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.IntegerField()


class TestMetricFileValue(models.Model):
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('MetricValue', on_delete=models.CASCADE)


class TestMetricBooleanValue(models.Model):
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.BooleanField()
