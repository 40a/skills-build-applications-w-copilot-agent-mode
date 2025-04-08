from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date
from django.contrib.auth.hashers import make_password
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Enforce stricter cleanup by resetting the database
        User.objects.filter(pk__isnull=False).delete()
        Team.objects.filter(pk__isnull=False).delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Ensure users are created only if they do not already exist
        for user_data in [
            {'username': 'thundergod', 'email': 'thundergod@mhigh.edu', 'password': 'password1'},
            {'username': 'metalgeek', 'email': 'metalgeek@mhigh.edu', 'password': 'password2'},
            {'username': 'zerocool', 'email': 'zerocool@mhigh.edu', 'password': 'password3'},
            {'username': 'crashoverride', 'email': 'crashoverride@mhigh.edu', 'password': 'password4'},
            {'username': 'sleeptoken', 'email': 'sleeptoken@mhigh.edu', 'password': 'password5'},
        ]:
            User.objects.filter(username=user_data['username']).delete()  # Remove duplicates
            user, created = User.objects.get_or_create(username=user_data['username'], defaults={
                'id': ObjectId(),  # Explicitly set ObjectId
                'email': user_data['email'],
                'password': make_password(user_data['password']),
            })

        # Ensure all users are saved before adding them to teams
        for user in User.objects.all():
            user.save()
            self.stdout.write(self.style.SUCCESS(f"User saved: {user.username}, ID: {user.id}"))

        # Debugging output to verify user primary keys
        for user in User.objects.all():
            self.stdout.write(self.style.SUCCESS(f"User: {user.username}, ID: {user.id}"))

        # Create teams
        team1 = Team(name='Blue Team')
        team2 = Team(name='Gold Team')
        team1.save()
        team2.save()

        # Assign members to teams
        team1.members.add(*User.objects.filter(username__in=['thundergod', 'metalgeek', 'zerocool']))  # First three users in Blue Team
        team2.members.add(*User.objects.filter(username__in=['crashoverride', 'sleeptoken']))  # Last two users in Gold Team

        # Retrieve saved users from the database
        saved_users = {user.username: user for user in User.objects.all()}

        # Debugging output to verify saved users
        self.stdout.write(self.style.SUCCESS(f"Saved users: {saved_users}"))

        # Explicitly query the database for each user when creating activities
        activities = [
            Activity(user=User.objects.get(username='thundergod'), activity_type='Cycling', duration=60, date=date(2025, 4, 8)),
            Activity(user=User.objects.get(username='metalgeek'), activity_type='Crossfit', duration=120, date=date(2025, 4, 7)),
            Activity(user=User.objects.get(username='zerocool'), activity_type='Running', duration=90, date=date(2025, 4, 6)),
            Activity(user=User.objects.get(username='crashoverride'), activity_type='Strength', duration=30, date=date(2025, 4, 5)),
            Activity(user=User.objects.get(username='sleeptoken'), activity_type='Swimming', duration=75, date=date(2025, 4, 4)),
        ]
        for activity in activities:
            activity.save()

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=team1, points=300),
            Leaderboard(team=team2, points=200),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event', duration=60),
            Workout(name='Crossfit', description='High-intensity interval training', duration=120),
            Workout(name='Running Training', description='Training for a marathon', duration=90),
            Workout(name='Strength Training', description='Weightlifting and strength exercises', duration=30),
            Workout(name='Swimming Training', description='Training for a swimming competition', duration=75),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
