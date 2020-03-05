from django.contrib import admin

from ctf.models import *


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ['name', 'members']
    list_display = ('name', 'contest', 'active', 'score', 'secret')
    list_filter = ('contest',)
    fields = [('contest', 'active'), ('name'), ('members'), ('secret')]
    filter_horizontal = ('members',)
    readonly_fields = ['secret']


class FlagInline(admin.TabularInline):
    model = Flag
    fields = [('name'), ('flag'), ('points'), ('penalty'), ('hint')]


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ('name', 'category', 'points', 'flag_count', 'active')
    list_filter = ('category',)
    fields = [('contest', 'active'),('sponsored','sponsor'), ('name', 'category'), ('link', 'dynamic_link'), ('file'),('minio_file_id')]
    inlines = [FlagInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    search_fields = ['team']
    list_display = ('team', 'flag', 'time', 'correct', 'guess', 'hinted')
    list_filter = ('team', 'correct')


# Register models
admin.site.register(Contest)
admin.site.register(Sponsor)
admin.site.register(Sponsorship)

