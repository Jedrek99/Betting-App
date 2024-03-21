import pytest
from django.test import Client
from django.urls import reverse

from bettingApp.forms import BetForm
from bettingApp.models import Bet


@pytest.mark.django_db
def test_bet_create_get(user_staff):
    client = Client()
    client.force_login(user_staff)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_bet_create_get_not_staff(user_not_staff):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_bet_create_post(user_staff, game):
    client = Client()
    client.force_login(user_staff)
    url = reverse('home')
    data = {'game_id': game.pk, 'user': user_staff.id, 'score': 1}
    response = client.post(url, data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_bet_create_post_not_staff(user_not_staff, game):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('home')
    data = {'game_id': game.pk, 'user': user_not_staff.id, 'score': 1}
    response = client.post(url, data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_game_create_get(user_staff, game):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addgame')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_game_create_get_not_staff(user_not_staff, game):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('addgame')
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_game_create_post(user_staff, game):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addgame')
    data = {'league': game.league.id, 'homeTeam': game.homeTeam.id, 'awayTeam': game.awayTeam.id, 'gametime': game.gametime}
    response = client.post(url, data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_add_score_get(user_staff, game):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addscore')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_score_get_not_staff(user_not_staff, game):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('addscore')
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_add_score_post(user_staff, game):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addscore')
    data = {'game_id': game.pk, 'score': 1}
    response = client.post(url, data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_score_post_not_staff(user_not_staff, game):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('addscore')
    data = {'game_id': game.pk, 'score': 1}
    response = client.post(url, data)
    assert response.status_code == 403