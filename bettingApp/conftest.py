from datetime import timedelta
from django.utils import timezone

from bettingApp.models import *
from django.contrib.auth.models import User
import pytest

@pytest.fixture
def country():
    return Country.objects.create(name='China')

@pytest.fixture
def league(country):
    return League.objects.create(id=1, name='Test League', country=country)

@pytest.fixture
def team(league):
    team = Team.objects.create(name='Test Team 1')
    team.league.add(league)
    return team

@pytest.fixture
def team2(league):
    team2 = Team.objects.create(name='Test Team 2')
    team2.league.add(league)
    return team2

@pytest.fixture
def user_staff():
    return User.objects.create_user(username='test', password='user', is_staff=True)

@pytest.fixture
def user_not_staff():
    return User.objects.create_user(username='test', password='user')


@pytest.fixture
def game(league, team, team2):
    gametime = timezone.now() + timedelta(days=2)
    return Game.objects.create(league=league, homeTeam=team, awayTeam=team2, gametime=gametime)