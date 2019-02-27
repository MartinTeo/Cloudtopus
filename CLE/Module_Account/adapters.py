# from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from  django.http import HttpResponseRedirect
from django.conf import settings
from django.dispatch import receiver
from django.contrib import messages
import re
from django.urls import reverse
from Module_TeamManagement.models import Student
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
from allauth.account.signals import user_signed_up



class SocialAccountWhitelist(DefaultSocialAccountAdapter):

    def get_connect_redirect_url(self, request, socialaccount):
        assert request.user.is_authenticated

        path = "instructor/home/"
        return path


    # This method overwrites the child class to populate user log in in database
    '''
    def populate_user(self,
                      request,
                      sociallogin,
                      data):
        pass
    '''

    def pre_social_login(self, request, sociallogin):
        email_address = sociallogin.account.extra_data["email"].split('@')[1]

        #use for team's test using any gmail account w/o numbers infront
        #isInstructor = re.findall(r"(^[a-zA-Z.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",sociallogin.account.extra_data["email"])

        #uncomment below for usage on staff email
        isInstructor = re.findall(r"(^[a-zA-Z.]+@smu.edu.sg+$)",sociallogin.account.extra_data["email"])

        # Pretty much hard code the login redirect url as the overwriting method above does not seem to be work
        if isInstructor != [] or sociallogin.account.extra_data["email"] in ("keagenkoi@gmail.com","rafaelbarros@smu.edu.sg","wendytanlc@smu.edu.sg","paulgriffin@smu.edu.sg","michellekan@smu.edu.sg","albertkeagen@gmail.com","hekamaru@gmail.com"):
            #print("Pushing to instructor's home")
            settings.LOGIN_REDIRECT_URL = "TMmod:instHome2"

        elif not email_address == "smu.edu.sg":
            messages.error(request, "Please use an SMU account")
            raise ImmediateHttpResponse(HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL))

        else:
            #print("Pushing to student's home")
            try:
                stu = Student.objects.get(email=sociallogin.account.extra_data["email"])
                stu.loginCounts += 1
                stu.save()
                settings.LOGIN_REDIRECT_URL = "TMmod:home"
            except:
                messages.error(request, "SMU Account is not registered for Cloudtopus")
                raise ImmediateHttpResponse(HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL))
