from django.contrib import admin

from .models import Athlete, School, Competitions, Result, DistanceToDay, Distance

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'rank', 'coach')
    search_fields = ('first_name', 'last_name')
    list_filter = ('rank', )

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(Competitions)
class CompetitionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_begin', 'date_end')
    search_fields = ('name', 'date_begin', 'date_end')

@admin.register(DistanceToDay)
class DistanceToDayAdmin(admin.ModelAdmin):
    list_display = ('competitions', 'distance', 'day', 'order')
    search_fields = ('competitions', 'day')

@admin.register(Distance)
class DistanceAdmin(admin.ModelAdmin):
    list_display = ('distance', 'style', 'sex')
    search_fields = ('distance', 'style', 'sex')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('time', )
    #search_fields = ('distancetoday', )

    
