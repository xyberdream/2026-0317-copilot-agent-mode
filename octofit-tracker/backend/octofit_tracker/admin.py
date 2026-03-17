from django.contrib import admin

from .models import Activity, LeaderboardEntry, Team, TrackerUser, Workout


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(TrackerUser)
class TrackerUserAdmin(admin.ModelAdmin):
    list_display = ('hero_alias', 'full_name', 'email', 'team', 'joined_at')
    list_filter = ('team',)
    search_fields = ('hero_alias', 'full_name', 'email')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'activity_type',
        'user',
        'duration_minutes',
        'calories_burned',
        'performed_at',
    )
    list_filter = ('activity_type', 'performed_at')
    search_fields = ('activity_type', 'user__hero_alias', 'user__full_name')


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user', 'points')
    list_filter = ('rank',)
    search_fields = ('user__hero_alias', 'user__full_name')


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'difficulty', 'duration_minutes', 'recommended_for')
    list_filter = ('difficulty',)
    search_fields = ('title', 'user__hero_alias', 'user__full_name', 'recommended_for')
