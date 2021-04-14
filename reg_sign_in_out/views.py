from django.shortcuts import render
from reg_sign_in_out.models import *
from . import forms 

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

import os
from face_att.settings import STATIC_DIR
import re




@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('reg_sign_in_out:user_login'))

@csrf_protect
@login_required
def registration(request):

    registered = False

    if request.method == "POST":
        form = forms.UserForm(request.POST)

        if form.is_valid():

            old = User.objects.filter(username='admin')
            
            if len(old)==1:
                old[0].delete()


            user = form.save()
            user.set_password(user.password)
            user.save()

            registered = True
            return HttpResponseRedirect(reverse('reg_sign_in_out:user_login'))
        
        else:

            print(form.errors)
            
            return render(request,"reg_sign_in_out/registration.html",{"tried":"True",
                                                    "registered":registered,
                                                   "user_form":form,
                                                   "errorone":form.errors,
                                                   })
            

    else:
        user = forms.UserForm()

    return render(request,"reg_sign_in_out/registration.html",{"registered":registered,
                                                   "user_form":user,
                                                   })


@csrf_protect
def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if username == "admin":
                    return HttpResponseRedirect(reverse('reg_sign_in_out:registration'))
                return HttpResponseRedirect(reverse('hq:new_entry'))

        else:

            return render(request,"reg_sign_in_out/login.html",{'tried':'True'})

    else:
        return render(request,"reg_sign_in_out/login.html")

