from django.db import models


# Create your models here.

class Sites(models.Model):
    location = models.TextField()
    title = models.TextField()
    start_date = models.DateField(name='startdate')
    end_date = models.DateField(name='enddate')
    description = models.TextField()
    price = models.IntegerField()
    link = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'sites'
