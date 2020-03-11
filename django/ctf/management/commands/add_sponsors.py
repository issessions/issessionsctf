import logging
from ctf.models import Sponsorship, Sponsor, Contest
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

class Command(BaseCommand):
    help = 'Sync teams from the LDAP server to the Postgresql DB'
    def handle(self, *args, **options):
        #initalize the contest

        #if( Contest.objects.all() == None ):
        #    logging.debug("no Contest")
          
        new_contest = Contest()
        new_contest.name = "ctf2020"
        new_contest.active = True
        new_contest.save()

        trend = Sponsor()
        trend.logo = File(open('trend.png', 'rb'))
        trend.name = "Trend Micro"
        trend.text = "hello"
        trend.save()

        bell = Sponsor()
        bell.logo = File(open('bell.png', 'rb'))
        bell.name = "Bell"
        bell.save()

        deloitte = Sponsor()
        deloitte.logo = File(open('deloite.png', 'rb'))
        deloitte.name = "Deloitte"
        deloitte.save()

        compass = Sponsor()
        compass.logo = File(open('compass.png', 'rb'))
        compass.name = "Security Compass"
        compass.save()

        vontel = Sponsor()
        vontel.logo = File(open('vontel.png', 'rb'))
        vontel.name = "Vontel"
        vontel.save()

        sheridan = Sponsor()
        sheridan.logo = File(open('sheridan.png', 'rb'))
        sheridan.name = "Sheridan College"
        sheridan.save()

        ssu = Sponsor()
        ssu.logo = File(open('ssu.png', 'rb'))
        ssu.name = "SSU"
        ssu.save()
        
        trend_title = Sponsorship()
        trend_title.contest = new_contest
        trend_title.sponsor = trend
        trend_title.tier = "TITLE"
        trend_title.save()

        bell_plat = Sponsorship()
        bell_plat.contest = new_contest
        bell_plat.sponsor = bell
        bell_plat.tier = "PLATINUM"
        bell_plat.save()
        
        deloitte_plat = Sponsorship()
        deloitte_plat.contest = new_contest
        deloitte_plat.sponsor = deloitte
        deloitte_plat.tier = "PLATINUM"
        deloitte_plat.save()
        
        compass_gold = Sponsorship()
        compass_gold.contest = new_contest
        compass_gold.sponsor = compass
        compass_gold.tier = "GOLD"
        compass_gold.save()

        vontel_comm = Sponsorship()
        vontel_comm.contest = new_contest
        vontel_comm.sponsor = vontel
        vontel_comm.tier = "COMMUNITY"
        vontel_comm.save()

        sheridan_comm = Sponsorship()
        sheridan_comm.contest = new_contest
        sheridan_comm.sponsor = sheridan
        sheridan_comm.tier = "COMMUNITY"
        sheridan_comm.save()

        ssu_comm = Sponsorship()
        ssu_comm.contest = new_contest
        ssu_comm.sponsor = ssu
        ssu_comm.tier = "COMMUNITY"
        ssu_comm.save()




