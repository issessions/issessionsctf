from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic

from ctf.models import Challenge, Submission, Team


def scoreboard(request):
    template_name = 'ctf/scoreboard.html'
    team_list = Team.objects.all().order_by('-score')
    for team in team_list:
        team.solved_count = team.solved.count()
    context = {'team_list': team_list}
    context['scoreboard_page'] = "active"
    return render(request, 'ctf/scoreboard.html', context)


def ctflogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        pass
    response = HttpResponse(status=302)
    response['Location'] = '/'
    return response


class ChallengeIndexView(LoginRequiredMixin, generic.ListView):
    login_url = "/"
    context_object_name = 'challenge_list'

    def get_queryset(self):
        challenge_list = Challenge.objects.order_by('category')
        return challenge_list

    def get_context_data(self, **kwargs):
        context = super(ChallengeIndexView, self).get_context_data(**kwargs)
        context['challenge_page'] = "active"
        return context


class ChallengeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Challenge
    login_url = "/"

    def get_context_data(self, **kwargs):
        context = super(ChallengeDetailView, self).get_context_data(**kwargs)
        context['challenge_page'] = "active"
        context['team'] = self.request.user.profile.current_team
        return context


@login_required(login_url="scoreboard")
def submit_flag(request, pk):
    team = request.user.profile.current_team
    challenge = Challenge.objects.get(pk=pk)
    if challenge not in team.solved.all():
        if challenge.flag == request.POST['flag']:
            messages.add_message(request, messages.SUCCESS, "You got the flag!")
            team.solved.add(challenge)
            team.score += challenge.points
            team.score_last = timezone.now()
            challenge.last_solved = timezone.now()
            challenge.solved += 1
            team.save()
            solution = Submission(team=team, challenge=challenge, new_score=team.score, correct=True)
            solution.save()
            challenge.save()
        else:
            if not Submission.objects.filter(team=team, challenge=challenge, correct=True).exists():
                solution = Submission(team=team, challenge=challenge, correct=False)
                solution.save()
                messages.add_message(request, messages.WARNING, "Wrong flag!")
    else:
        # They've already solved it
        messages.add_message(request, messages.INFO, "Your team has already solved this challenge")

    return redirect(request.META['HTTP_REFERER'])
