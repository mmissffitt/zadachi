from django.db import models

class Tags(models.Model):
    name = models.CharField(max_length=100)

class Tasks(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, blank=True)
