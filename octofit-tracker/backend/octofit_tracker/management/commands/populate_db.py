from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        # Clear all collections using MongoDB directly
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client.octofit_db
        
        collections = ['activities', 'teams', 'leaderboard', 'workouts', 'octofit_tracker_user']
        for collection in collections:
            db[collection].delete_many({})

        with transaction.atomic():
            # Create users
            users_data = [
                {'username': 'thundergod', 'email': 'thundergod@mhigh.edu', 'password': 'password1'},
                {'username': 'metalgeek', 'email': 'metalgeek@mhigh.edu', 'password': 'password2'},
                {'username': 'zerocool', 'email': 'zerocool@mhigh.edu', 'password': 'password3'},
                {'username': 'crashoverride', 'email': 'crashoverride@mhigh.edu', 'password': 'password4'},
                {'username': 'sleeptoken', 'email': 'sleeptoken@mhigh.edu', 'password': 'password5'},
            ]
            
            users = []
            for user_data in users_data:
                user = User.objects.create(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=make_password(user_data['password'])
                )
                users.append(user)
                self.stdout.write(f"Created user: {user.username}")

            # Create teams
            team1 = Team.objects.create(name='Blue Team')
            team2 = Team.objects.create(name='Gold Team')
            self.stdout.write("Created teams")

            # Add members to teams
            team1.members.add(*users[:3])  # First three users in Blue Team
            team2.members.add(*users[3:])  # Last two users in Gold Team
            self.stdout.write("Added members to teams")

            # Create activities
            activities_data = [
                {'user': users[0], 'activity_type': 'Cycling', 'duration': 60, 'date': date(2025, 4, 8)},
                {'user': users[1], 'activity_type': 'Crossfit', 'duration': 120, 'date': date(2025, 4, 7)},
                {'user': users[2], 'activity_type': 'Running', 'duration': 90, 'date': date(2025, 4, 6)},
                {'user': users[3], 'activity_type': 'Strength', 'duration': 30, 'date': date(2025, 4, 5)},
                {'user': users[4], 'activity_type': 'Swimming', 'duration': 75, 'date': date(2025, 4, 4)},
            ]

            for activity_data in activities_data:
                activity = Activity.objects.create(**activity_data)
                self.stdout.write(f"Created activity: {activity}")

            # Create leaderboard entries
            Leaderboard.objects.create(team=team1)
            Leaderboard.objects.create(team=team2)
            self.stdout.write("Created leaderboard entries")

            # Create workouts
            workouts_data = [
                {'name': 'Morning Cardio', 'description': 'Start your day with energy', 'duration': 30},
                {'name': 'Strength Training', 'description': 'Build muscle and power', 'duration': 45},
                {'name': 'HIIT Session', 'description': 'High-intensity interval training', 'duration': 25},
            ]

            for workout_data in workouts_data:
                workout = Workout.objects.create(**workout_data)
                self.stdout.write(f"Created workout: {workout}")

            self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
