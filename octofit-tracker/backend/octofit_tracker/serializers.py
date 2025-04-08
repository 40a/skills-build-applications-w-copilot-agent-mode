from rest_framework import serializers
from bson import ObjectId
from .models import User, Team, Activity, Leaderboard, Workout

class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return ObjectId(data)

class UserSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)

    class Meta:
        model = User
        fields = ['_id', 'username', 'email']

class TeamSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    total_points = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = ['_id', 'name', 'members', 'total_points']

class ActivitySerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    user = UserSerializer(read_only=True)
    user_id = ObjectIdField(write_only=True, source='user._id')

    class Meta:
        model = Activity
        fields = ['_id', 'user', 'user_id', 'activity_type', 'duration', 'date', 'points']

class LeaderboardSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    team = TeamSerializer(read_only=True)
    team_id = ObjectIdField(write_only=True, source='team._id')

    class Meta:
        model = Leaderboard
        fields = ['_id', 'team', 'team_id', 'points', 'last_updated']

class WorkoutSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)

    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'duration']
