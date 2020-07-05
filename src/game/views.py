from django.shortcuts import render

# Create your views here.
from game.models import Match


def home(request):
    open_matches = Match.objects.filter(state=Match.MatchState.OPEN)
    in_progress = Match.objects.filter(state=Match.MatchState.STARTED)
    completed = Match.objects.filter(state=Match.MatchState.COMPLETED)

    return render(request, 'home.html',
                  {'open': open_matches,
                   'in_progress': in_progress,
                   'completed': completed})
