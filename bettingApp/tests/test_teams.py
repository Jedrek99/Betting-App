import pytest
from django.test import Client
from django.urls import reverse

from bettingApp.forms import TeamForm
from bettingApp.models import Team

@pytest.mark.django_db
def test_teamlist_view_get():
    url = reverse('teamlist')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_teamlist_view_post(league):
    url = reverse('teamlist')
    client = Client()
    data = {'league': league.id}
    response = client.post(url, data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_addteam_view_get_staff(user_staff):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addteam')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], TeamForm)

@pytest.mark.django_db
def test_addteam_view_get_not_staff(user_not_staff):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('addteam')
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_addteam_view_post_staff(user_staff, league):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addteam')
    data = {'name': 'Test Team 1', 'league': league.id}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Team.objects.get(name='Test Team 1')

@pytest.mark.django_db
def test_deleteteam_view_get_staff(user_staff, league):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addteam')
    data = {'name': 'Test Team 1', 'league': league.id}
    response = client.post(url, data)
    assert response.status_code == 302
    url = reverse('deleteteam', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['team'].name == 'Test Team 1'

@pytest.mark.django_db
def test_deleteteam_view_get_not_staff(user_not_staff, team):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('deleteteam', kwargs={'pk': team.pk})
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_deleteteam_view_post(user_staff, league):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addteam')
    data = {'name': 'Test Team 1', 'league': league.id}
    response = client.post(url, data)
    team = Team.objects.get(name='Test Team 1')
    url = reverse('deleteteam', kwargs={'pk': 1})
    data = {'action': 'yes'}
    response = client.post(url, data)
    assert response.status_code == 302
    with pytest.raises(Team.DoesNotExist):
        Team.objects.get(pk=team.pk)


@pytest.mark.django_db
def test_editteam_view_get(user_staff, league):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addteam')
    data = {'name': 'Test Team 1', 'league': league.id}
    response = client.post(url, data)
    team = Team.objects.get(name='Test Team 1')
    url = reverse('editteam', kwargs={'pk': team.pk})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_editteam_view_get_not_staff(user_not_staff, team):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('editteam', kwargs={'pk': team.pk})
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_editteam_view_post(user_staff, league):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addteam')
    data = {'name': 'Test Team 1', 'league': league.id}
    response = client.post(url, data)
    team = Team.objects.get(name='Test Team 1')
    url = reverse('editteam', kwargs={'pk': team.pk})
    data = {'name': 'Test Team 2', 'league': league.id}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Team.objects.get(name='Test Team 2')