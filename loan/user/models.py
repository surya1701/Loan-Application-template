from django.db import models

# Create your models here.
class Prediction(models.Model):
    uname = models.CharField(max_length=100)
    gender = models.CharField(max_length=6)
    married = models.CharField(max_length=3)
    depend = models.CharField(max_length=2)
    education = models.CharField(max_length=12)
    self_employ = models.CharField(max_length=3)
    aincome = models.IntegerField()
    caincome = models.IntegerField()
    loanamt = models.IntegerField()
    loanterm = models.IntegerField()
    credhist = models.IntegerField()
    area = models.CharField(max_length=9)
    pred = models.CharField(max_length=1, default='-1')