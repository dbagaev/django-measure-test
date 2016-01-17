from django.db import models

from pyxperiment.metric import Metric as exp_Metric


# Create your models here.
class ExperimentSet(models.Model):
    Type = models.CharField(max_length=128)

    def Experiments(self):
        return Experiment.objects.filter(ExperimentSet=self)

    def __str__(self) :
        return self.Type

    def Metrics(self):
        return Metric.objects.filter(ExperimentSet=self).order_by('Name')

    @staticmethod
    def findByName(name) :
        return ExperimentSet.objects.filter(Type=name)[:1].get()


class Experiment(models.Model):
    Name = models.CharField(max_length=256)
    ExperimentSet = models.ForeignKey('ExperimentSet', on_delete=models.CASCADE)

    def Metrics(self):
        return Metric.objects.filter(Experiment=self).order_by('Name')


    def __str__(self) :
        return self.Name + " @ " + self.ExperimentSet.Type



class Run(models.Model):
    Started = models.TimeField(auto_now=True)

    @property
    def ExperimentSetRuns(self) :
        return ExperimentSetRun.objects.filter(Run=self)

class ExperimentSetRun(models.Model) :
    Started = models.TimeField(auto_now=True)
    Run = models.ForeignKey('Run', on_delete=models.CASCADE)
    ExperimentSet = models.ForeignKey('ExperimentSet', on_delete=models.CASCADE)

    @property
    def Values(self) :
        return MetricValue.objects.filter(ExperimentSetRun=self, ExperimentRun=None).prefetch_related().order_by("Metric__Name")

    @property
    def ExperimentRuns(self) :
        return ExperimentRun.objects.filter(ExperimentSetRun=self)


class ExperimentRun(models.Model):
    Started = models.TimeField(auto_now=True)
    Success = models.IntegerField(default=True)
    Run = models.ForeignKey('Run', on_delete=models.CASCADE)
    ExperimentSetRun = models.ForeignKey('ExperimentSetRun', on_delete=models.CASCADE)
    Experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE)

    @property
    def Values(self) :
        return MetricValue.objects.filter(ExperimentRun=self).prefetch_related().order_by("Metric__Name")


class Metric(models.Model):
    VALUE_TYPES = (
        (exp_Metric.TYPE_FLOAT, 'Float'),
        (exp_Metric.TYPE_INTEGER, 'Integer'),
        (exp_Metric.TYPE_BOOLEAN, 'Boolean'),
        (exp_Metric.TYPE_STRING, 'String'),
        (exp_Metric.TYPE_FILE, 'File')
    )

    Name = models.CharField(max_length=64)
    Type = models.IntegerField(choices=VALUE_TYPES)
    Accumulator = models.BooleanField(default=False)

    ExperimentSet = models.ForeignKey('ExperimentSet', on_delete=models.CASCADE)

    def __str__(self) :
        return self.ExperimentSet.Type + " :: " + self.Name

class MetricValue(models.Model):
    ExperimentRun = models.ForeignKey('ExperimentRun', on_delete=models.CASCADE, db_constraint=False, null=True)
    ExperimentSetRun = models.ForeignKey('ExperimentSetRun', on_delete=models.CASCADE)
    Run = models.ForeignKey('Run', on_delete=models.CASCADE)
    Metric = models.ForeignKey('Metric', on_delete=models.CASCADE)

    @property
    def Value(self) :
        try :
            if self.Metric.Type == exp_Metric.TYPE_FLOAT :
                v = MetricFloatValue.objects.filter(MetricValue=self)[:1].get()
                return v.Value
            elif self.Metric.Type == exp_Metric.TYPE_INTEGER :
                v = MetricIntegerValue.objects.filter(MetricValue=self)[:1].get()
                return v.Value
            elif self.Metric.Type == exp_Metric.TYPE_STRING :
                v = MetricStringValue.objects.filter(MetricValue=self)[:1].get()
                return v.Value
            elif self.Metric.Type == exp_Metric.TYPE_BOOLEAN :
                v = MetricBooleanValue.objects.filter(MetricValue=self)[:1].get()
                return v.Value
            else :
                return None
        except :
            return None

    @property
    def toStr(self) :
        return str(self.Value)


class MetricStringValue(models.Model):
    MetricValue = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.CharField(max_length=256)


class MetricFloatValue(models.Model):
    MetricValue = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.FloatField()


class MetricIntegerValue(models.Model):
    MetricValue = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.IntegerField()


class MetricFileValue(models.Model):
    MetricValue = models.ForeignKey('MetricValue', on_delete=models.CASCADE)


class MetricBooleanValue(models.Model):
    MetricValue = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.BooleanField()
