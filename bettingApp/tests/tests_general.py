import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_get():
    url = reverse('home')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_homepage_post(league):
    client = Client()
    url = reverse('home')
    data = {'league': league.pk}
    response = client.post(url, data)
    assert response.status_code == 200


def test_createuser_get():
    client = Client()
    url = reverse('createuser')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_createuser_post():
    client = Client()
    url = reverse('createuser')
    data = {'username': 'user', 'password': '123', 'password2': '123'}
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_createuser_post_diff_password():
    client = Client()
    url = reverse('createuser')
    data = {'username': 'user', 'password': '123', 'password2': '1234'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == 'Different passwords'

@pytest.mark.django_db
def test_login_get():
    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_post():
    client = Client()
    url = reverse('createuser')
    data = {'username': 'user', 'password': '123', 'password2': '123'}
    response = client.post(url, data)
    assert response.status_code == 302
    url = reverse('login')
    data = {'username': 'user', 'password': '123'}
    response = client.post(url, data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_login_post_wrong_password():
    client = Client()
    url = reverse('createuser')
    data = {'username': 'user', 'password': '123', 'password2': '123'}
    response = client.post(url, data)
    assert response.status_code == 302
    url = reverse('login')
    data = {'username': 'user', 'password': '1234'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == 'Incorrect data!'

@pytest.mark.django_db
def test_logout_get(user_staff):
    client = Client()
    client.force_login(user_staff)
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_userview_get(user_staff):
    client = Client()
    client.force_login(user_staff)
    url = reverse('userview')
    response = client.get(url)
    assert response.status_code == 200
