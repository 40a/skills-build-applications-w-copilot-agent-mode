from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data safely
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create users
        users = [
            User(username='thundergod', email='thundergod@mhigh.edu', password='password1'),
            User(username='metalgeek', email='metalgeek@mhigh.edu', password='password2'),
            User(username='zerocool', email='zerocool@mhigh.edu', password='password3'),
            User(username='crashoverride', email='crashoverride@mhigh.edu', password='password4'),
            User(username='sleeptoken', email='sleeptoken@mhigh.edu', password='password5'),
        ]

        # Save users to the database
        for user in users:
            user.save()

        # Create teams
        team1 = Team(name='Blue Team')
        team2 = Team(name='Gold Team')
        team1.save()
        team2.save()

        # Assign members to teams
        team1.members.add(*users[:3])  # First three users in Blue Team
        team2.members.add(*users[3:])  # Last two users in Gold Team

        # Save activities with proper user references
        activities = [
            Activity(user=User.objects.get(username='thundergod'), activity_type='Cycling', duration=60, date=date(2025, 4, 8)),
            Activity(user=User.objects.get(username='metalgeek'), activity_type='Crossfit', duration=120, date=date(2025, 4, 7)),
            Activity(user=User.objects.get(username='zerocool'), activity_type='Running', duration=90, date=date(2025, 4, 6)),
            Activity(user=User.objects.get(username='crashoverride'), activity_type='Strength', duration=30, date=date(2025, 4, 5)),
            Activity(user=User.objects.get(username='sleeptoken'), activity_type='Swimming', duration=75, date=date(2025, 4, 4)),
        ]
        Activity.objects.bulk_create(activities)

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
