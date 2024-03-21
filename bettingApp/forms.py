from django import forms
from django.core.exceptions import ValidationError

from bettingApp.models import *


class TeamListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeamListForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    class Meta:
        model = Team
        fields = '__all__'


class LeagueListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LeagueListForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    class Meta:
        model = League
        fields = '__all__'

class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = '__all__'
        widgets = {
            'league': forms.CheckboxSelectMultiple
        }

class LeagueForm(forms.ModelForm):

    class Meta:
        model = League
        fields = '__all__'

class CountryForm(forms.ModelForm):

    class Meta:
        model = Country
        fields = '__all__'

class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        exclude = {'score'}
        widgets = {
            'gametime': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }

class GameFilterForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = {'league'}

class BetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].choices = [(value, label) for value, label in self.fields['score'].choices if value or value == 0]

    class Meta:
        model = Bet
        fields = ['score']
        widgets = {
            'score': forms.RadioSelect()
        }

class ScoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].choices = [(value, label) for value, label in self.fields['score'].choices if value or value == 0]

    class Meta:
        model = Game
        fields = ['score']
        widgets = {
            'score': forms.RadioSelect()
        }