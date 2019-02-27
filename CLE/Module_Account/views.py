from django.shortcuts import render
from django.shortcuts import redirect
from Module_Account.src import processLogin
from  django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from allauth.account.views import LogoutView

# LOGIN VALIDATION -----------------------------------------------------------#
def login_view(requests):
    result = {}
    if requests.method == "GET":
        return render(requests, "Module_Account/login.html", result)

    # If not GET, then proceed
    try:
        username = requests.POST.get("username")
        password = requests.POST.get("password")

        # Proceed to validating of username and password
        user = processLogin.validate(username,password)

    except Exception as e:

        return render(requests, "Module_Account/login.html", {"error" : str(e)})

    if user != None :
        login(requests,user,backend='django.contrib.auth.backends.ModelBackend')
        return render(requests, "Administrator/admindashboard.html", result)

    else:
        #HttpResponseRedirect(('TMmod:home'))
        return render(requests, "Module_Account/login.html", result)

# LOGOUT ---------------------------------------------------------------------#
#@login_required(login_url='/')
def logout_view(requests):
    logout(requests)
    return redirect("/")


logout = LogoutView.as_view() #This is from allauth logout [Fixes the session problem]