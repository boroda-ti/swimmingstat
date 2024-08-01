from django.contrib import admin

from .models import Athlete, Coach, Manager

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'rank', 'coach')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('rank', )

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'rank')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('rank', )

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')