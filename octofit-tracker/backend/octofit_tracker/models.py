from djongo import models
from bson import ObjectId

class User(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

class Team(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=100)
    members = models.ArrayReferenceField(to=User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name

    def update_total_points(self):
        member_ids = [str(member._id) for member in self.members.all()]
        activities = Activity.objects.filter(user__in=self.members.all())
        self.total_points = sum(activity.points for activity in activities)
        self.save()

class Activity(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='_id')
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    date = models.DateField()
    points = models.IntegerField(default=0)

    class Meta:
        db_table = 'activities'

    def save(self, *args, **kwargs):
        self.points = self.calculate_points()
        super().save(*args, **kwargs)
        self.update_team_points()

    def calculate_points(self):
        # Basic point calculation: 1 point per minute
        return self.duration

    def update_team_points(self):
        teams = Team.objects.filter(members=self.user)
        for team in teams:
            team.update_total_points()

    def __str__(self):
        return f"{self.activity_type} by {self.user.username}"

class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    team = models.OneToOneField(Team, on_delete=models.CASCADE, to_field='_id')
    points = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'

    def update_points(self):
        self.points = self.team.total_points
        self.save()

    def __str__(self):
        return f"{self.team.name}: {self.points} points"

class Workout(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()  # in minutes

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name
