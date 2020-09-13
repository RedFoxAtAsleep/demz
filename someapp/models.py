from django.db import models


# Create your models here.
class Memo(models.Model):
    content = models.CharField(max_length=256, null=True)
    content = models.TextField(max_length=1024, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Link(models.Model):
    url = models.CharField(max_length=1024, null=True)
    remark = models.TextField(max_length=1024, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)




