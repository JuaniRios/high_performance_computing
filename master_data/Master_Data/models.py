from django.db import models
from django.utils import timezone
from django.core.validators import int_list_validator


# Database models for the master data service
class Job(models.Model):
    class Meta:
        verbose_name = 'job'
        verbose_name_plural = 'jobs'

    owner = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    class Status(models.IntegerChoices):
        SUBMITTED = 1, 'Submitted'
        PROCESSING = 2, 'Processing'
        DONE = 3, 'Done'

    status = models.IntegerField(choices=Status.choices)
    date_range = models.DateField()
    assets = models.CharField(validators=[int_list_validator], max_length=10000)


class Result(models.Model):
    class Meta:
        verbose_name = "result"
        verbose_name_plural = "results"

    job = models.ForeignKey(Job, related_name="results", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    assets = models.CharField(validators=[int_list_validator], max_length=10000)
    weights = models.CharField(validators=[int_list_validator], max_length=10000)
