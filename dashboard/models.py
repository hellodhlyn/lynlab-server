# -*- coding: utf-8 -*-

from django.db import models

class BusDashboard(models.Model):
    class Meta:
        verbose_name = u'busdashboard'
        ordering = ['bus_id']
    
    bus_id = models.CharField(max_length=10)
    bus_number = models.CharField(max_length=10)
    station_id = models.CharField(max_length=10)
    station_name = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.bus_id