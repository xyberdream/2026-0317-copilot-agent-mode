from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class TrackerUser(models.Model):
    full_name = models.CharField(max_length=100)
    hero_alias = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name='members',
        null=True,
        blank=True,
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.hero_alias} ({self.full_name})'


class Activity(models.Model):
    user = models.ForeignKey(TrackerUser, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    performed_at = models.DateTimeField()

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return f'{self.activity_type} - {self.user.hero_alias}'


class LeaderboardEntry(models.Model):
    user = models.OneToOneField(
        TrackerUser,
        on_delete=models.CASCADE,
        related_name='leaderboard_entry',
    )
    points = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'leaderboard'

    def __str__(self):
        return f'#{self.rank} {self.user.hero_alias} ({self.points} pts)'


class Workout(models.Model):
    user = models.ForeignKey(TrackerUser, on_delete=models.CASCADE, related_name='workouts')
    title = models.CharField(max_length=120)
    difficulty = models.CharField(max_length=30)
    duration_minutes = models.PositiveIntegerField()
    recommended_for = models.CharField(max_length=255)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return f'{self.title} ({self.user.hero_alias})'