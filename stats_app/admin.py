from django.contrib import admin

from .models import Athlete, School

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'rank', 'coach')
    search_fields = ('first_name', 'last_name')
    list_filter = ('rank', )

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
