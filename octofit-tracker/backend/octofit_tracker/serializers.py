from rest_framework import serializers

from .models import Activity, LeaderboardEntry, Team, TrackerUser, Workout


class StringPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return str(value.pk)


class BaseStringIdSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.pk)


class TeamSerializer(BaseStringIdSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description']


class TrackerUserSerializer(BaseStringIdSerializer):
    team = StringPrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = TrackerUser
        fields = ['id', 'full_name', 'hero_alias', 'email', 'team', 'joined_at']


class ActivitySerializer(BaseStringIdSerializer):
    user = StringPrimaryKeyRelatedField(queryset=TrackerUser.objects.all())

    class Meta:
        model = Activity
        fields = ['id', 'user', 'activity_type', 'duration_minutes', 'calories_burned', 'performed_at']


class LeaderboardEntrySerializer(BaseStringIdSerializer):
    user = StringPrimaryKeyRelatedField(queryset=TrackerUser.objects.all())

    class Meta:
        model = LeaderboardEntry
        fields = ['id', 'user', 'points', 'rank']


class WorkoutSerializer(BaseStringIdSerializer):
    user = StringPrimaryKeyRelatedField(queryset=TrackerUser.objects.all())

    class Meta:
        model = Workout
        fields = ['id', 'user', 'title', 'difficulty', 'duration_minutes', 'recommended_for']