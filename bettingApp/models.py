from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

CHOICES = (
    (1, 1), (0, 0), (2, 2))


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class League(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    name = models.CharField(max_length=50)
    league = models.ManyToManyField(League)

    def __str__(self):
        return f"{self.name}"


class Game(models.Model):
    league = models.ForeignKey(League, default=None, on_delete=models.CASCADE)
    homeTeam = models.ForeignKey(Team, default=1, related_name='home_games', on_delete=models.CASCADE)
    awayTeam = models.ForeignKey(Team, default=2, related_name='away_games', on_delete=models.CASCADE)
    gametime = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(choices=CHOICES, default=None, null=True, blank=True)



class Bet(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=CHOICES)

