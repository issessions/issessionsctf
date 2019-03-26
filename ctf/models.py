from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils import timezone


class Sponsor(models.Model):
    """A company or organization who sponsored this competition."""

    name = models.CharField(max_length=256)
    text = models.TextField()
    logo = models.FileField(upload_to='sponsor_logos/', blank=True)


class Contest(models.Model):
    """The Contest"""

    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=timezone.now)
    stop_time = models.DateTimeField(default=timezone.now)
    sponsors = models.ManyToManyField(Sponsor, blank=True, through='Sponsorship')

    def save(self, *args, **kwargs):
        # TODO: Make sure only one contest is "active"
        super().save(*args, **kwargs)

    @staticmethod
    def current() -> "Contest":
        try:
            return Contest.objects.get(active=True)
        except Contest.DoesNotExist:
            return None


class Sponsorship(models.Model):
    """Sponsorship for a company for a specific contest"""

    tiers = (
        ('TITLE', 'Title Sponsor'),
        ('GOLD', 'Gold Sponsor'),
        ('SILVER', 'Silver Sponsor'),
        ('BRONZE', 'Bronze Sponsor')
    )

    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    tier = models.CharField(max_length=20, choices=tiers)


class Profile(models.Model):
    """ Extending User model to add extra per-user features.
        A Profile represents a player.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @property
    def current_team(self):
        try:
            return self.user.teams.get(contest__active=True)
        except Team.DoesNotExist:
            return None


# Creating Signals to automatically create Profiles when users are created
@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Flag(models.Model):
    name = models.CharField(max_length=200)
    flag = models.CharField(max_length=50, blank=False)
    points = models.IntegerField()
    hint = models.TextField()
    penalty = models.IntegerField()
    solved = models.IntegerField(default=0)
    last_solved = models.DateTimeField(blank=True, null=True)


class Challenge(models.Model):
    categories = (
        ('PROGRAMMING', 'Programming'),
        ('CRYPTOGRAPHY', 'Cryptography'),
        ('PACKETANALYSIS', 'Packet Analysis'),
        ('TRIVIA', 'Trivia'),
        ('WEBAPP', 'Web App'),
        ('DATABASE', 'Database'),
        ('SYSADMIN', 'SysAdmin'),
        ('STEGANOGRAPHY', 'Steganography'),
        ('REVERSING', 'Reversing'),
        ('LOCKPICKING', 'Lockpicking'),
        ('FORENSICS', 'Forensics'))

    contest = models.ForeignKey(Contest, related_name="challenges", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=categories)
    link = models.URLField(blank=True, default="")
    file = models.FileField(upload_to='uploads/', blank=True)
    active = models.BooleanField(default=True)

    @staticmethod
    def current(**kwargs):
        """Filter active competitions."""

        return Challenge.objects.filter(contest__active=True, **kwargs)


class Team(models.Model):
    # Competition
    contest = models.ForeignKey(Contest, related_name="teams", on_delete=models.CASCADE)

    # Team members
    members = models.ManyToManyField(User, blank=True, related_name="teams")

    # Which problems this team has solved
    solved = models.ManyToManyField(Challenge, blank=True, related_name="solvers")

    # Information about team
    name = models.CharField(max_length=64)
    active = models.BooleanField(default=False)

    score = models.IntegerField(default=0)
    score_last = models.DateTimeField(default=timezone.now)

    # Meta model attributes
    class Meta:
        ordering = ("-score", "score_last")

    def __str__(self):
        return self.name

    @staticmethod
    def current(**kwargs):
        """Filter active competitions."""

        return Team.objects.filter(contest__active=True, **kwargs)


class Submission(models.Model):
    """A submission for a problem."""

    # Link to team and problem
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='solves')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='solves')

    # Time and correctness
    time = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)

    # Guess and new score
    guess = models.CharField(max_length=128, default="")
    new_score = models.IntegerField(default=0)

    class Meta:
        ordering = ('time',)

    def __str__(self):
        return "{} submitted {} at {}".format(self.team, self.challenge, self.time)
