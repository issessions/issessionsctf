from django import forms

class NewPasswordForm(forms.Form):
    oldPassword = forms.CharField(widget=forms.PasswordInput())
    newPassword = forms.CharField(widget=forms.PasswordInput())
    newPasswordConf = forms.CharField(widget=forms.PasswordInput())   

class ForgotPasswordForm(forms.Form):
    newPassword = forms.CharField(widget=forms.PasswordInput())
    newPasswordConf = forms.CharField(widget=forms.PasswordInput())

class JoinTeamForm(forms.Form):
    join_code = forms.CharField(max_length=30)

class CreateTeamForm(forms.Form):
    team_name = forms.CharField(max_length=64,min_length=1,required=True,label='Team Name')

class EditTeamForm(forms.Form):
    new_team_name = forms.CharField(max_length=64,min_length=1,required=True,label='New Team Name')
