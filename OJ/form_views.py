from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from OJ.forms import *
from OJ.models import User

# 注册表单提交
def register_post(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm = form.cleaned_data['confirm']
            school = form.cleaned_data['school']
            student_id = form.cleaned_data['student_id']
            gender = form.cleaned_data['gender']

            if password == confirm:
                try:
                    User.objects.create_user(username, email, password, school, student_id, gender)
                except IntegrityError as registerException:
                    try:
                        transaction.rollback()
                    except Exception as rollbackException:
                        pass
                    return HttpResponse(str('已经有人用这个邮箱注册过了'))

                return HttpResponseRedirect(reverse('login'))
            else:
                return HttpResponse(str('两次输入的密码不一致'))
        else:
            return HttpResponse(str('输入的信息不符合要求'))
    else:
        return HttpResponseRedirect(reverse('index'))

# 登录表单提交
def login_post(request):
    if request.method == 'POST':
        form = LogginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse(str('邮箱或者密码打错啦'))
        else:
            return HttpResponse(str('好像输入了奇怪的东西……'))
    else:
        return HttpResponseRedirect(reverse('index'))

# 注销
def logout_get(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))