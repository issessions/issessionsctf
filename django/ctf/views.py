import magic
import mimetypes
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
import hashlib
import logging
import base64
from django.views import generic
from minio import Minio
from minio.error import ResponseError, NoSuchKey, NoSuchBucket
from urllib3.exceptions import MaxRetryError
from django_auth_ldap.backend import LDAPBackend
from ctf.ldap_ops import LDAPOperator
from ctf.forms import NewPasswordForm, CreateTeamForm, EditTeamForm, JoinTeamForm
import pyotp
from .forms import NewPasswordForm, CreateTeamForm, EditTeamForm, JoinTeamForm
from .models import Challenge, Submission, Team, Flag, Sponsorship, Sponsor

from django.conf import settings


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
    #print("hello"+sponsorships_list[1].sponsor.name)
    context = {'sponsorship_list': sponsorships_list}
    return render(request,'ctf/sponsors.html',context)
    
def help_tools(request):
    return render(request, 'ctf/help-tools.html')

def help_tutorials(request):
    return render(request, 'ctf/help-tutorials.html')

def help_other(request):
    return render(request, 'ctf/help-other.html')

def team_management(request):
    ldap_object = LDAPOperator() 
    result_set = ldap_object.find_ldap_teams()
    context = {"users":result_set}
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
        my_team = self.request.user.profile.current_team
        context['team'] = my_team

        current_challenge = context['challenge']
        context['sysadmin_url'] = "not a sysadmin chal"
        if (current_challenge.category == "sysadmin"):
            #generate a otp using the team secret as the seed
            team_secret = my_team.secret
            challenge_name = current_challenge.name
            team_name = my_team.name
            totp = pyotp.TOTP(base64.b32encode(team_secret.encode()),interval=600)
            my_totp = totp.now()
            logging.debug(my_totp)
            #concatinate the challenge name, team, and otp, this is the value you use int the url
            valueToHash = challenge_name + team_name + my_totp
            url_hash = hashlib.sha256(valueToHash.encode('utf-8'))  #.encode('utf-8')
            url_hash = url_hash.hexdigest()
            team_name_hash= hashlib.sha256(team_name.encode())
            team_name_hash = team_name_hash.hexdigest()
            sysadmin_url = "sysadmin-api-url.com/" + challenge_name + '/' + str(team_name_hash)[0:10] + '/' + self.request.user.username + '/' + str( url_hash )  
            logging.debug(sysadmin_url)   
            context['sysadmin_url'] = sysadmin_url
        #checking to see if hint should be sent
        flag_objects = current_challenge.flags.all()
        hints = my_team.hints.filter(challenge=current_challenge)
        already_hinted = False
        the_hint = "Reminder: Viewing the hint reduces the number of points a challenge is worth."

        for f in flag_objects:
            if f in hints:
                already_hinted = True
                the_hint = f.hint
            else:
                pass
        if already_hinted:
            context['hint'] = the_hint
        else:
            pass
            ####
        if (current_challenge.sponsored):
            challenge_sponsor = current_challenge.sponsor
            context['sponsor'] = challenge_sponsor

        return context

@login_required(login_url="scoreboard")
def reveal_hint(request, pk):
    current_challenge = Challenge.objects.get(pk=pk)
    team = request.user.profile.current_team
    flag_objects = current_challenge.flags.all()
    flag_list = [flag_object for flag_object in flag_objects]
    hints = team.hints.filter(challenge=current_challenge)
    already_hinted = False
    for f in flag_objects:
        if f in hints:
            already_hinted = True
        else:
            pass
    if already_hinted:
        return redirect(request.META['HTTP_REFERER'])
    else:
        for f in flag_list: 
            team.hints.add(f)
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url="scoreboard")
def submit_flag(request, pk):

    submission = request.POST['flag']  # User Submission
    team = request.user.profile.current_team  # User's Team (If Any)
    challenge = Challenge.objects.get(pk=pk)  # Challenge
    flag_objects = challenge.flags.all()  # All flag objects associated with the challenge
    flag_list = [flag_object.flag for flag_object in flag_objects]  # All flag strings associated with the challenge
    solved = submission in flag_list  # Successfully solved or not
    hint_used = False
    hints = team.hints.filter(challenge=challenge)
    for f in flag_objects:
        if f in hints:
            hint_used = True
            flag_penalty = f.penalty
        else:
            pass
    #print(flag_penalty)

    if team is None:  # If user is authenticated but not part of a team
        messages.add_message(request, messages.WARNING, "You must be on a team to submit a flag!")
        return redirect(request.META['HTTP_REFERER'])

    if challenge is None:  # situation not possible through GUI, protects against arbitrary submissions
        messages.add_message(request, messages.WARNING, "Challenge does not exist!")
        return redirect(request.META['HTTP_REFERER'])

    if solved:  # If the challenge is successfully solved
        solved_flag = flag_objects.get(flag=submission)  # retrieve the associated flag object
        if solved_flag not in team.solved.all():  # If the team has not secured this flag before
            team.solved.add(solved_flag)  
            if hint_used:
                team.score += solved_flag.points - flag_penalty
            else:
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


@login_required(login_url='scoreboard')
def download(request, minio_bucket, minio_file_id):

    # Initialize initial Minio Client Object
    client = Minio(getattr(settings, 'MINIO_HOST'),
                   access_key=getattr(settings, 'MINIO_ACCESS_KEY'),
                   secret_key=getattr(settings, 'MINIO_SECRET_KEY'),
                   secure=False)

    # Make 2 requests for the file:
    # Note: one request is not possible because it is not possible to rewind a live stream of bytes
    try:

        # Request #1: stream a small byte sample to determine file mimetype/proper extension
        data = client.get_object(minio_bucket, minio_file_id)
        sample = data.read(amt=256)
        mime_sniffer = magic.Magic(mime=True)
        mime_type = mime_sniffer.from_buffer(sample)
        file_extension = mimetypes.guess_extension(type=mime_type)  # With leading dot (.zip)
        data.close()

        # Request #2: stream the whole file to facilitate its download
        data = client.get_object(minio_bucket, minio_file_id)
        response = StreamingHttpResponse(streaming_content=data, content_type=mime_type)
        response['Content-Disposition'] = 'attachment;filename=' + minio_file_id + file_extension
        return response

    except NoSuchKey as nsk:
        messages.add_message(request, messages.WARNING, "File Not Found.")
    except NoSuchBucket as nsb:
        messages.add_message(request, messages.WARNING, "Bucket Not Found.")
    except MaxRetryError as mre:
        messages.add_message(request, messages.WARNING, "Multiple attempts to contact MinIO file server have failed.")
    except ResponseError as rspe:
        messages.add_message(request, messages.WARNING, "HTTP Response Error.")
    #except Exception as e:
        #messages.add_message(request, messages.WARNING, "An internal error has occurred.")

    print(request.META)
    return redirect(to='challenge-index')


