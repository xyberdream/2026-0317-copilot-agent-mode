from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Activity, LeaderboardEntry, Team, TrackerUser, Workout


class CollectionApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(
            name='Avengers',
            description='Earth heroes team',
        )
        cls.user = TrackerUser.objects.create(
            full_name='Tony Stark',
            hero_alias='Iron Man',
            email='ironman@octofit.test',
            team=cls.team,
        )
        cls.activity = Activity.objects.create(
            user=cls.user,
            activity_type='HIIT',
            duration_minutes=42,
            calories_burned=500,
            performed_at=timezone.now() - timedelta(days=1),
        )
        cls.leaderboard_entry = LeaderboardEntry.objects.create(
            user=cls.user,
            points=970,
            rank=1,
        )
        cls.workout = Workout.objects.create(
            user=cls.user,
            title='Arc Reactor Endurance',
            difficulty='Hard',
            duration_minutes=55,
            recommended_for='Total body endurance',
        )

    def _find_by_id(self, payload, object_id):
        expected_id = str(object_id)
        return next((item for item in payload if item['id'] == expected_id), None)

    def test_api_root_includes_all_collections(self):
        response = self.client.get('/api/')
        payload = response.json()
        root_response = self.client.get('/')
        root_payload = root_response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('base_url', payload)
        self.assertIn('users', payload)
        self.assertIn('teams', payload)
        self.assertIn('activities', payload)
        self.assertIn('leaderboard', payload)
        self.assertIn('workouts', payload)

        self.assertEqual(root_response.status_code, status.HTTP_200_OK)
        self.assertEqual(root_payload, payload)

    def test_users_collection_uses_string_ids_and_allows_create(self):
        list_response = self.client.get('/api/users/')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        existing = self._find_by_id(list_response.data, self.user.pk)
        self.assertIsNotNone(existing)
        self.assertEqual(existing['team'], str(self.team.pk))

        create_payload = {
            'full_name': 'Peter Parker',
            'hero_alias': 'Spider-Man',
            'email': 'spiderman@octofit.test',
            'team': str(self.team.pk),
        }
        create_response = self.client.post('/api/users/', create_payload, format='json')

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data['team'], str(self.team.pk))

    def test_teams_collection_returns_string_ids(self):
        response = self.client.get('/api/teams/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        team_payload = self._find_by_id(response.data, self.team.pk)
        self.assertIsNotNone(team_payload)
        self.assertEqual(team_payload['name'], self.team.name)

    def test_activities_collection_returns_user_as_string_id(self):
        response = self.client.get('/api/activities/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        activity_payload = self._find_by_id(response.data, self.activity.pk)
        self.assertIsNotNone(activity_payload)
        self.assertEqual(activity_payload['user'], str(self.user.pk))

    def test_leaderboard_collection_returns_user_as_string_id(self):
        response = self.client.get('/api/leaderboard/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        leaderboard_payload = self._find_by_id(response.data, self.leaderboard_entry.pk)
        self.assertIsNotNone(leaderboard_payload)
        self.assertEqual(leaderboard_payload['user'], str(self.user.pk))

    def test_workouts_collection_returns_user_as_string_id(self):
        response = self.client.get('/api/workouts/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        workout_payload = self._find_by_id(response.data, self.workout.pk)
        self.assertIsNotNone(workout_payload)
        self.assertEqual(workout_payload['user'], str(self.user.pk))
