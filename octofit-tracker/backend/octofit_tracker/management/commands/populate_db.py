from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from octofit_tracker.models import Activity, LeaderboardEntry, Team, TrackerUser, Workout


class Command(BaseCommand):
    help = 'octofit_db 데이터베이스에 테스트 데이터를 입력합니다.'

    def handle(self, *args, **options):
        self.stdout.write('기존 테스트 데이터 정리 중...')
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        LeaderboardEntry.objects.all().delete()
        TrackerUser.objects.all().delete()
        Team.objects.all().delete()

        marvel = Team.objects.create(name='marvel 팀', description='마블 히어로 팀')
        dc = Team.objects.create(name='dc 팀', description='DC 히어로 팀')

        users = {
            'iron_man': TrackerUser.objects.create(
                full_name='Tony Stark',
                hero_alias='Iron Man',
                email='ironman@octofit.test',
                team=marvel,
            ),
            'spider_man': TrackerUser.objects.create(
                full_name='Peter Parker',
                hero_alias='Spider-Man',
                email='spiderman@octofit.test',
                team=marvel,
            ),
            'batman': TrackerUser.objects.create(
                full_name='Bruce Wayne',
                hero_alias='Batman',
                email='batman@octofit.test',
                team=dc,
            ),
            'wonder_woman': TrackerUser.objects.create(
                full_name='Diana Prince',
                hero_alias='Wonder Woman',
                email='wonderwoman@octofit.test',
                team=dc,
            ),
        }

        now = timezone.now()
        Activity.objects.bulk_create(
            [
                Activity(
                    user=users['iron_man'],
                    activity_type='HIIT',
                    duration_minutes=45,
                    calories_burned=520,
                    performed_at=now - timedelta(days=1),
                ),
                Activity(
                    user=users['spider_man'],
                    activity_type='Parkour Run',
                    duration_minutes=30,
                    calories_burned=360,
                    performed_at=now - timedelta(days=2),
                ),
                Activity(
                    user=users['batman'],
                    activity_type='Strength Training',
                    duration_minutes=50,
                    calories_burned=610,
                    performed_at=now - timedelta(days=1, hours=2),
                ),
                Activity(
                    user=users['wonder_woman'],
                    activity_type='Combat Cardio',
                    duration_minutes=40,
                    calories_burned=480,
                    performed_at=now - timedelta(days=3),
                ),
            ]
        )

        LeaderboardEntry.objects.bulk_create(
            [
                LeaderboardEntry(user=users['batman'], points=980, rank=1),
                LeaderboardEntry(user=users['iron_man'], points=940, rank=2),
                LeaderboardEntry(user=users['wonder_woman'], points=900, rank=3),
                LeaderboardEntry(user=users['spider_man'], points=860, rank=4),
            ]
        )

        Workout.objects.bulk_create(
            [
                Workout(
                    user=users['iron_man'],
                    title='Arc Reactor Endurance Circuit',
                    difficulty='Hard',
                    duration_minutes=55,
                    recommended_for='전신 지구력 및 코어 강화',
                ),
                Workout(
                    user=users['spider_man'],
                    title='Wall-Crawl Agility Session',
                    difficulty='Medium',
                    duration_minutes=35,
                    recommended_for='민첩성 및 하체 폭발력 향상',
                ),
                Workout(
                    user=users['batman'],
                    title='Gotham Tactical Strength Block',
                    difficulty='Hard',
                    duration_minutes=60,
                    recommended_for='근력 및 기능성 움직임 최적화',
                ),
                Workout(
                    user=users['wonder_woman'],
                    title='Amazonian Power Flow',
                    difficulty='Medium',
                    duration_minutes=45,
                    recommended_for='근지구력과 밸런스 강화',
                ),
            ]
        )

        self.stdout.write(self.style.SUCCESS('octofit_db 테스트 데이터 적재 완료'))