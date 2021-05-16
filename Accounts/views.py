from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from Accounts.models import Account
from django.contrib.auth.models import auth
from django.contrib.auth.hashers import make_password, check_password

import random
import os
from django.conf import settings
from django.http import HttpResponse, Http404


# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        sponsor = request.POST.get('sponsor')
        mobile_no = request.POST.get('mobile')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        # pass2 = request.POST.get('pass2')
        fName = request.POST.get('fName')
        # lName = request.POST.get('lName')

        pass12 = make_password(pass1)

        try:
            spn_obj = Account.objects.get(username=sponsor)
            while True:
                rand_num = random.randint(500000, 599999)
                u_name = 'LDM' + str(rand_num)
                if Account.objects.filter(username=u_name).exists():
                    pass
                else:
                    break

            user = Account(username=u_name, sponsor=spn_obj,
                           password=pass12, email=email,
                           txn_password="pass2", phon_no=mobile_no,
                           rem_pass=pass1, first_name=fName,
                           last_name="lName")
            #obj.downline = u_name

            user.save()

            request.session['user_name'] = u_name
            request.session['spn'] = spn_obj.username
            request.session['u_pass'] = pass1
            request.session['txn_pass'] = "pass2"

            user = auth.authenticate(username=u_name, password=pass1)
            if user is not None:
                auth.login(request, user)

                messages.success(request, 'Update Profile First!!')
                # file_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics/app-release.apk')
                # if os.path.exists(file_path):
                #     with open(file_path, 'rb') as fh:
                #         response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                #         response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                #         return response
                # raise Http404
                return redirect('detail')

        except Exception as e:
            print(e)
            messages.error(request, "Sponsor Does Not Exist!!")
            return redirect('signup')

    else:
        pass

    return render(request, 'signup.html')


@login_required
def detail(request):
    username = request.session['user_name']
    sponsor = request.session['spn']
    u_pass = request.session['u_pass']
    txn_pass = request.session['txn_pass']
    user_obj = Account.objects.get(username=username)
    spn_obj = Account.objects.get(username=sponsor)

    d = {
        'username': username,
        'sponsor': sponsor,
        'user_obj': user_obj,
        'spn_obj': spn_obj,
        'u_pass': u_pass,
        'txn_pass': txn_pass,
    }
    return render(request, 'detail.html', d)


@csrf_exempt
def login1(request):
    if request.method == 'POST':
        u_name = request.POST.get('user_name')
        pass1 = request.POST.get('pass_word')

        user = auth.authenticate(username=u_name, password=pass1)

        if user is not None:
            auth.login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Wrong username or password!!')
            return redirect('login')

    return render(request, 'login.html')
