from djongo import models
from django.contrib.auth.models import User

class User(models.Model):
    id = models.ObjectIdField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Team(models.Model):
    id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="teams")

    def __str__(self):
        return self.name

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    date = models.DateField()

    def __str__(self):
        return f"{self.activity_type} by {self.user.username}"

class Leaderboard(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, to_field='id')
    points = models.IntegerField()

    def __str__(self):
        return f"{self.team.name}: {self.points} points"

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()  # in minutes

    def __str__(self):
        return self.name
