from datetime import datetime
import pytz
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from bettingApp.forms import TeamListForm, LeagueListForm, CountryForm, LeagueForm, TeamForm, GameForm, GameFilterForm, BetForm, ScoreForm
from bettingApp.models import Team, League, Country, Game, Bet


def has_common_league(leagues1, leagues2):
    for league in leagues1:
        if league in leagues2:
            return True
    return False

class HomePage(View):
    def get(self, request):
        games = Game.objects.filter(gametime__gt=datetime.now()).order_by('gametime')
        leagues = League.objects.all()
        form = GameFilterForm()
        form2 = BetForm()
        return render(request, 'home.html', {'games': games, 'leagues': leagues, 'form': form, 'form2': form2})

    def post(self, request):
        if 'league' in request.POST and request.POST['league']:
            leagues = request.POST['league']
            games = Game.objects.filter(gametime__gt=datetime.now(), league=leagues).order_by('gametime')
            form = GameFilterForm(request.POST)
            form2 = BetForm()
            return render(request, 'home.html', {'games': games, 'leagues': leagues, 'form': form, 'form2': form2})
        elif 'score' in request.POST:
            form = BetForm(request.POST)
            if form.is_valid():
                user = request.user
                score = form.cleaned_data['score']
                game_id = request.POST['game_id']
                if Bet.objects.filter(game_id=game_id, user=user).exists():
                    games = Game.objects.filter(gametime__gt=datetime.now()).order_by('gametime')
                    leagues = League.objects.all()
                    form = GameFilterForm()
                    form2 = BetForm()
                    return render(request, 'home.html',
                                  {'games': games, 'leagues': leagues, 'form': form, 'form2': form2,
                                   'error': 'You have already bet on this game'})
                print(game_id)
                Bet.objects.create(user=user, game_id=game_id, score=score)
                games = Game.objects.filter(gametime__gt=datetime.now()).order_by('gametime')
                leagues = League.objects.all()
                form = GameFilterForm()
                form2 = BetForm()
                return render(request, 'home.html', {'games': games, 'leagues': leagues, 'form': form, 'form2': form2})
class TeamListView(View):
    def get(self, request):
        leagues = League.objects.all()
        teams = Team.objects.all()
        teams = teams.order_by('name')
        form = TeamListForm()
        return render(request, 'teamlist.html', {'teams': teams, 'form': form, 'leagues': leagues})

    def post(self, request):
        teams = Team.objects.all()
        leagues = League.objects.all()
        name = request.POST.get('name')
        if name:
            teams = teams.filter(name__icontains=name)
            leagues = []
            for team in teams:
                leagues.append(team.league)
            leagues = set(leagues)
        searched_league = request.POST.get('league')
        if searched_league:
            try:
                teams = teams.filter(league=searched_league)
                teams = teams.order_by('name')
                leagues = leagues.filter(pk=searched_league)
            except AttributeError:
                pass
        form = TeamListForm(request.POST)
        return render(request, 'teamlist.html', {'teams': teams, 'form': form, 'leagues': leagues})

class LeagueListView(View):
    def get(self, request):
        leagues = League.objects.all()
        countries = Country.objects.all()
        countries = countries.order_by('name')
        form = LeagueListForm()
        return render(request, 'leaguelist.html', {'leagues': leagues, 'form': form, 'countries': countries})

    def post(self, request):
        countries = Country.objects.all()
        leagues = League.objects.all()
        name = request.POST.get('name')
        if name:
            leagues = leagues.filter(name__icontains=name)
            countries = []
            for league in leagues:
                countries.append(league.country)
            countries = set(countries)
            countries = countries
        searched_country = request.POST.get('country')
        if searched_country:
            leagues = leagues.filter(country=searched_country)
            countries = countries.filter(pk=searched_country)
            countries = countries.order_by('name')
        form = LeagueListForm()
        return render(request, 'leaguelist.html', {'countries': countries, 'form': form, 'leagues': leagues})

class AddTeamView(UserPassesTestMixin, View):

    def test_func(self):
        user = self.request.user
        is_staff = User.objects.filter(is_staff=True)
        return user in is_staff

    def get(self, request):
        form = TeamForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.name = team.name.title()
            team.save()
            league_ids = form.cleaned_data.get('league').values_list('id', flat=True)
            if league_ids:
                team.league.set(league_ids)
            return redirect('teamlist')
        return render(request, 'form.html', {'form': form})
class AddLeagueView(UserPassesTestMixin, View):

    def test_func(self):
        user = self.request.user
        is_staff = User.objects.filter(is_staff=True)
        return user in is_staff
    def get(self, request):
        form = LeagueForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = LeagueForm(request.POST)
        if form.is_valid():
            league = form.save(commit=False)
            league.name = form.cleaned_data['name'].title()
            league.country = form.cleaned_data['country']
            leagues = League.objects.all()
            leaguenames = [league.name for league in leagues]
            if league.name not in leaguenames:
                league.save()
            else:
                return render(request, 'form.html', {'form': form, 'error': 'League already in database!'})
        return redirect('leaguelist')

class AddCountryView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        is_staff = User.objects.filter(is_staff=True)
        return user in is_staff
    def get(self, request):
        form = CountryForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = CountryForm(request.POST)
        if form.is_valid():
            country = form.save(commit=False)
            country.name = form.cleaned_data['name'].title()
            countries = Country.objects.all()
            countrynames = [country.name for country in countries]
            if country.name not in countrynames:
                country.save()
            else:
                return render(request, 'form.html', {'form':form, 'error': 'Country already in database!'})
        return redirect('leaguelist')

class AddGameView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        is_staff = User.objects.filter(is_staff=True)
        return user in is_staff
    def get(self, request):
        form = GameForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.league = form.cleaned_data['league']
            game.home_team = form.cleaned_data['homeTeam']
            game.away_team = form.cleaned_data['awayTeam']
            game.gametime = form.cleaned_data['gametime']
            team1 = Team.objects.get(name=form.cleaned_data['homeTeam'])
            team2 = Team.objects.get(name=form.cleaned_data['awayTeam'])
            leagues1 = Team.objects.filter(name=form.cleaned_data['homeTeam']).values_list('league', flat=True)
            leagues2 = Team.objects.filter(name=form.cleaned_data['awayTeam']).values_list('league', flat=True)
            game_time = game.gametime.replace(tzinfo=pytz.UTC)
            if game_time > datetime.now().replace(tzinfo=pytz.UTC):
                if game.home_team == game.away_team:
                    return render(request, 'form.html', {'form': form, 'errors': 'Choose two different teams'})
                elif game.league.id not in leagues1 or game.league.id not in leagues2:
                    return render(request, 'form.html', {'form': form, 'errors': 'Choose valid league!'})
                elif not has_common_league(leagues1, leagues2):
                    return render(request, 'form.html', {'form': form, 'errors': 'Teams must play in the same league'})
                else:
                    game.save()
                    return redirect('home')
            else:
                return render(request, 'form.html', {'form': form, 'errors': 'Game was already played!'})

class EditTeamView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        is_staff = User.objects.filter(is_staff=True)
        return user in is_staff
    def get(self, request, pk):
        try:
            team = Team.objects.get(pk=pk)
            form = TeamForm(instance=team)
            selected_leagues = team.league.all()
            form.fields['league'].initial = selected_leagues
            return render(request, 'form.html', {'form': form})
        except Team.DoesNotExist:
            return redirect(request, 'home')

    def post(self, request, pk):
        team = Team.objects.get(pk=pk)
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.name = team.name.title()
            form.save()
            return redirect('teamlist')
        return render(request, 'form.html', {'form':form, 'error': 'Incorrect data!'})

class EditLeagueView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        is_staff = User.objects.filter(is_staff=True)
        return user in is_staff
    def get(self, request, pk):
        try:
            league = League.objects.get(pk=pk)
            form = LeagueForm(instance=league)
            return render(request, 'form.html', {'form': form})
        except League.DoesNotExist:
            return redirect('home')

    def post(self, request, pk):
        league = League.objects.get(pk=pk)
        form = LeagueForm(request.POST, instance=league)
        if form.is_valid():
            league = form.save(commit=False)
            league.name = league.name.title()
            league.save()
            return redirect('leaguelist')
        return render(request, 'form.html', {'form':form, 'error': 'Incorrect data!'})

class EditCountryView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        is_staff = User.objects.filter(is_staff=True)
        return user in is_staff
    def get(self, request, pk):
        try:
            country = Country.objects.get(pk=pk)
            form = CountryForm(instance=country)
            return render(request, 'form.html', {'form': form})
        except Country.DoesNotExist:
            return redirect('home')

    def post(self, request, pk):
        country = Country.objects.get(pk=pk)
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            country = form.save(commit=False)
            country.name = country.name.title()
            form.save()
            return redirect('home')
        return render(request, 'form.html', {'form':form, 'error': 'Incorrect data!'})

class DeleteTeamView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        is_staff = User.objects.filter(is_staff=True)
        return user in is_staff
    def get(self, request, pk):
        try:
            team = Team.objects.get(pk=pk)
            return render(request, 'delete.html', {'team': team})
        except team.DoesNotExist:
            return redirect('home')

    def post(self, request, pk):
        option = request.POST.get('action')
        if option == 'yes':
            team = Team.objects.get(pk=pk)
            team.delete()
        return redirect('teamlist')

class DeleteLeagueView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        is_staff = User.objects.filter(is_staff=True)
        return user in is_staff
    def get(self, request, pk):
        try:
            league = League.objects.get(pk=pk)
            return render(request, 'delete.html', {'league': league})
        except League.DoesNotExist:
            return redirect('home')

    def post(self, request, pk):
        option = request.POST.get('action')
        if option == 'yes':
            league = League.objects.get(pk=pk)
            league.delete()
        return redirect('leaguelist')


class CreateUserView(View):

    def get(self, request):
        return render(request, 'createuser.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        re_password = request.POST['password2']
        if password != re_password:
            return render(request, 'createuser.html', {'error': 'Different passwords'})
        u = User(username=username)
        u.set_password(password)
        u.save()
        return redirect('login')

class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        url = request.GET.get('next', 'home')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(url)
        else:
            return render(request, 'login.html', {'error': 'Incorrect data!'})

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home')

class UserView(View):
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        bets = Bet.objects.filter(user=user)
        bets_with_score = Bet.objects.filter(user=user).exclude(score=None)
        games = [bet.game for bet in bets]
        won_bets = []
        lost_bets = []
        for game in games:
            bet = Bet.objects.get(game=game, user=request.user)
            if game.score == bet.score:
                won_bets.append(bet)
            elif game.score is not None and game.score != bet.score:
                lost_bets.append(bet)
        if len(bets) == 0:
            win_percentage = None
        else:
            win_percentage = len(won_bets)/len(bets_with_score) *100
        return render(request, 'userview.html', {'user': user, 'bets':bets, 'won_bets':won_bets, 'lost_bets':lost_bets, 'win_percentage': win_percentage})


class AddScoreToGameView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        is_staff = User.objects.filter(is_staff=True)
        return user in is_staff
    def get(self, request):
        games = Game.objects.filter(score=None).order_by('gametime')
        form = ScoreForm()
        return render(request, 'addscore.html', {'games': games, 'form':form})

    def post(self, request):
        form = ScoreForm(request.POST)
        if form.is_valid():
            game_id = request.POST['game_id']
            game = Game.objects.get(id=game_id)
            score = form.cleaned_data['score']
            game_time = game.gametime.replace(tzinfo=pytz.UTC)
            if game_time < datetime.now().replace(tzinfo=pytz.UTC):
                game.score = score
                game.save()
                games = Game.objects.filter(score=None)
                return render(request, 'addscore.html', {'games': games, 'form':form})
            else:
                games = Game.objects.filter(score=None)
                return render(request, 'addscore.html', {'games': games, 'form': form, 'error': 'You cannot enter score for game that has not yet been played!'})
        games = Game.objects.filter(score=None)
        return render(request, 'addscore.html', {'form': form, 'games':games, 'error': 'Invalid input'})
