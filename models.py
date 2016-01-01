from django.db import models

# Create your models here.
class Test(models.Model) :
    id = models.IntegerField(primary_key=True)
    Type = models.CharField(max_length=128)

class TestCase(models.Model) :
    id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=256)
    Test = models.ForeignKey('Test', on_delete=models.CASCADE)

class Run(models.Model) :
    id = models.IntegerField(primary_key=True)
    Started = models.TimeField()

class TestRun(models.Model) :
    id = models.IntegerField(primary_key=True)
    Started = models.TimeField()
    Success = models.IntegerField()
    Run = models.ForeignKey('Run', on_delete=models.CASCADE)
    Test = models.ForeignKey('TestCase', on_delete=models.CASCADE)

class TestMetric(models.Model) :
    VALUE_TYPES = (
        (0, 'Double'),
        (1, 'Integer'),
        (2, 'Boolean'),
        (3, 'String'),
        (4, 'File')
    )
    id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=64)
    Type = models.IntegerField(choices=VALUE_TYPES)
    Test = models.ForeignKey('Test', on_delete=models.CASCADE)

class TestCaseMetricValue(models.Model) :
    id = models.IntegerField(primary_key=True)
    TestMetric = models.ForeignKey('TestMetric', on_delete=models.CASCADE)
    TestCase = models.ForeignKey('TestCase', on_delete=models.CASCADE)
    TestRun = models.ForeignKey('TestRun', on_delete=models.CASCADE)

class TestMetricStringValue(models.Model) :
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('TestCaseMetricValue', on_delete=models.CASCADE)
    Value = models.CharField(max_length=256)

class TestMetricDoubleValue(models.Model) :
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('TestCaseMetricValue', on_delete=models.CASCADE)
    Value = models.FloatField()

class TestMetricIntegerValue(models.Model) :
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('TestCaseMetricValue', on_delete=models.CASCADE)
    Value = models.IntegerField()

class TestMetricFileValue(models.Model) :
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('TestCaseMetricValue', on_delete=models.CASCADE)

class TestMetricBooleanValue(models.Model) :
    id = models.IntegerField(primary_key=True)
    Metric = models.ForeignKey('TestCaseMetricValue', on_delete=models.CASCADE)
    Value = models.BooleanField()


