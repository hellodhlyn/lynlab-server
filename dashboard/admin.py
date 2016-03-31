# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import BusDashboard

class BusDashboardAdmin(admin.ModelAdmin):
    list_display = ['bus_number', 'bus_id', 'station_name', 'station_id']
    search_fields = ['bus_number']
    ordering = ['bus_number']

admin.site.register(BusDashboard, BusDashboardAdmin)