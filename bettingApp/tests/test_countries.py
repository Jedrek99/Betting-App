import pytest
from django.test import Client
from django.urls import reverse

from bettingApp.forms import CountryForm
from bettingApp.models import Country

@pytest.mark.django_db
def test_addcountry_view_get(user_staff):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addcountry')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], CountryForm)

@pytest.mark.django_db
def test_addcountry_view_get_not_staff(user_not_staff):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('addcountry')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_addcountry_view_post(user_staff):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addcountry')
    data = {'name': 'China'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Country.objects.get(name='China')

@pytest.mark.django_db
def test_editcountry_view_get(user_staff, country):
    client = Client()
    client.force_login(user_staff)
    url = reverse('editcountry', kwargs={'pk': country.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_editcountry_view_get_not_staff(user_not_staff, country):
    client = Client()
    client.force_login(user_not_staff)
    url = reverse('editcountry', kwargs={'pk': country.pk})
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_editcountry_view_post(user_staff, country):
    client = Client()
    client.force_login(user_staff)
    url = reverse('addcountry')
    data = {'name': country.name}
    response = client.post(url,data)
    url = reverse('editcountry', kwargs={'pk': country.pk})
    data = {'name': "Poland"}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Country.objects.filter(name='Poland').exists()