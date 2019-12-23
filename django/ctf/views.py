from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from django_auth_ldap.backend import LDAPBackend
from ctf.forms import NewPasswordForm, CreateTeamForm, EditTeamForm, JoinTeamForm

from ctf.models import Challenge, Submission, Team, Flag, Sponsorship, Sponsor


def scoreboard(request):
    template_name = 'ctf/scoreboard.html'
    team_list = Team.objects.filter(active=True).order_by('-score')
    for team in team_list:
        team.solved_count = team.solved.count()
    context = {'team_list': team_list}
    context['scoreboard_page'] = "active"
    return render(request, 'ctf/scoreboard.html', context)

def sponsors(request):
    sponsorships_list = Sponsorship.objects.all()
    print("hello"+sponsorships_list[1].sponsor.name)
    context = {'sponsorship_list': sponsorships_list}
    return render(request,'ctf/sponsors.html',context)

#def join_team(request):

#def create_team(request):

#def edit_team(request):

#def leave_team(request):

#def forgot_password(request):

def team_management(request):
    joinTeamForm = JoinTeamForm()
    createTeamForm = CreateTeamForm()
    editTeamForm = EditTeamForm() 
    context = {'join_form': joinTeamForm, 'create_form':createTeamForm, 'edit_form':editTeamForm}
    return render(request, 'ctf/team-management.html', context)

def change_password(request):
    if request.method == 'GET':
        form = NewPasswordForm()
    else:
        #do something! I SHOULD HAVE LDAP DONE BEFORE STARTING THIS
        form = NewPasswordForm()
    return render(request, 'ctf/new-password.html',{'form': form})


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
        challenge_list = Challenge.objects.filter(active=True).order_by('category')
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

    submission = request.POST['flag']  # User Submission
    team = request.user.profile.current_team  # User's Team (If Any)
    challenge = Challenge.objects.get(pk=pk)  # Challenge
    flag_objects = challenge.flags.all()  # All flag objects associated with the challenge
    flag_list = [flag_object.flag for flag_object in flag_objects]  # All flag strings associated with the challenge
    solved = submission in flag_list  # Successfully solved or not

    if team is None:  # If user is authenticated but not part of a team
        messages.add_message(request, messages.WARNING, "You must be on a team to submit a flag!")
        return redirect(request.META['HTTP_REFERER'])

    if challenge is None:  # situation not possible through GUI, protects against arbitrary submissions
        messages.add_message(request, messages.WARNING, "Challenge does not exist!")
        return redirect(request.META['HTTP_REFERER'])

    if solved:  # If the challenge is successfully solved
        solved_flag = flag_objects.get(flag=submission)  # retrieve the associated flag object
        if solved_flag not in team.solved.all():  # If the team has not secured this flag before
            team.solved.add(solved_flag)  #
            team.score += solved_flag.points
            team.score_last = timezone.now()
            solved_flag.last_solved = timezone.now()
            solved_flag.solved += 1
            solution = Submission(team=team, challenge=challenge, flag=solved_flag, correct=True)
            team.save()
            solved_flag.save()
            solution.save()
            messages.add_message(request, messages.SUCCESS, "You got the flag!")
        else:
            messages.add_message(request, messages.INFO, "Your team has already solved this challenge")
    else:
        solution = Submission(team=team, challenge=challenge, correct=False)  # record failed submissions too
        solution.save()
        messages.add_message(request, messages.WARNING, "Wrong flag!")

    return redirect(request.META['HTTP_REFERER'])

