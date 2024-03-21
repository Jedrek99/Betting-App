import pytest
from django.test import Client
from django.urls import reverse

from bettingApp.forms import LeagueForm
from bettingApp.models import League

@pytest.mark.django_db
def test_leaguelist_view_get():
    url = reverse('leaguelist')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_leaguelist_view_post(league):
    url = reverse('leaguelist')
    client = Client()
    data = {'league': league.id}
    response = client.post(url, data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_addleague_view_get(user_staff):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addleague')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], LeagueForm)

@pytest.mark.django_db
def test_addleague_view_get_not_staff(user_not_staff):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('addleague')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_addleague_view_post(user_staff, country):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addleague')
    data = {'name': 'Test League', 'country': country.id}
    response = client.post(url, data)
    assert response.status_code == 302
    assert League.objects.filter(name='Test League').exists()

@pytest.mark.django_db
def test_deleteleague_view_get(user_staff, league):
    client = Client()
    client.force_login(user_staff)
    url = reverse('deleteleague', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['league'] == league

@pytest.mark.django_db
def test_deleteleague_view_get_not_staff(user_not_staff, league):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('deleteleague', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_deleteleague_view_post(user_staff, league):
    client = Client()
    client.force_login(user_staff)
    url = reverse('deleteleague', kwargs={'pk': league.pk})
    data = {'action': 'yes'}
    response = client.post(url, data)
    assert response.status_code == 302
    with pytest.raises(League.DoesNotExist):
        League.objects.get(pk=league.pk)

@pytest.mark.django_db
def test_editleague_view_get(user_staff, league):
    client = Client()
    client.force_login(user_staff)
    url = reverse('editleague', kwargs={'pk': league.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_editleague_view_get_not_staff(user_not_staff, league):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('editleague', kwargs={'pk': league.pk})
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_editleague_view_post(user_staff, league):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addleague')
    data = {'name': league.name, 'country': league.country.id}
    response = client.post(url,data)
    url = reverse('editleague', kwargs={'pk': league.pk})
    data = {'name': "Test League 2", 'country': league.country.id}
    response = client.post(url, data)
    assert response.status_code == 302
    assert League.objects.filter(name='Test League 2').exists()
