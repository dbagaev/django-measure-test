from django.db import models
from MeasureTest.TestMetric import TestMetric

# Create your models here.
class Test(models.Model):
    id = models.IntegerField(primary_key=True)
    Type = models.CharField(max_length=128)

    def Cases(self):
        return TestCase.objects.filter(Test=self)

    def Metrics(self):
        return TestMetric.objects.filter(Test=self)


class TestCase(models.Model):
    id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=256)
    Test = models.ForeignKey('Test', on_delete=models.CASCADE)


class Run(models.Model):
    id = models.IntegerField(primary_key=True)
    Started = models.TimeField()


class TestRun(models.Model):
    id = models.IntegerField(primary_key=True)
    Started = models.TimeField()
    Success = models.IntegerField()
    Run = models.ForeignKey('Run', on_delete=models.CASCADE)
    Test = models.ForeignKey('TestCase', on_delete=models.CASCADE)


class TestMetric(models.Model):
    VALUE_TYPES = (
        (TestMetric.TYPE_FLOAT, 'Float'),
        (TestMetric.TYPE_INTEGER, 'Integer'),
        (TestMetric.TYPE_BOOLEAN, 'Boolean'),
        (TestMetric.TYPE_STRING, 'String'),
        (TestMetric.TYPE_FILE, 'File')
    )
    id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=64)
    Type = models.IntegerField(choices=VALUE_TYPES)
    Test = models.ForeignKey('Test', on_delete=models.CASCADE)


class TestCaseMetricValue(models.Model):
    id = models.IntegerField(primary_key=True)
    TestMetric = models.ForeignKey('TestMetric', on_delete=models.CASCADE)
    TestCase = models.ForeignKey('TestCase', on_delete=models.CASCADE)
    TestRun = models.ForeignKey('TestRun', on_delete=models.CASCADE)


class TestMetricStringValue(models.Model):
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('TestCaseMetricValue', on_delete=models.CASCADE)
    Value = models.CharField(max_length=256)


class TestMetricFloatValue(models.Model):
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('TestCaseMetricValue', on_delete=models.CASCADE)
    Value = models.FloatField()


class TestMetricIntegerValue(models.Model):
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('TestCaseMetricValue', on_delete=models.CASCADE)
    Value = models.IntegerField()


class TestMetricFileValue(models.Model):
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('TestCaseMetricValue', on_delete=models.CASCADE)


class TestMetricBooleanValue(models.Model):
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('TestCaseMetricValue', on_delete=models.CASCADE)
    Value = models.BooleanField()
