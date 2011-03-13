#!/usr/bin/env python
from django.contrib import admin
from states.models import LGA, State, Country

class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code',)

class LGAAdmin(admin.ModelAdmin):
    list_display = ('name','state')
    
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    

admin.site.register(State, StateAdmin)
admin.site.register(LGA, LGAAdmin)
admin.site.register(Country, CountryAdmin)