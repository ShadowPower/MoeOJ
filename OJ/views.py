from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from markdown import markdown


# Create your views here.
def index(request):
    return render(request, "index.html")

def problemset(request):
    return render(request, "problem/problemset.html")

def status(request):
    return render(request, "status.html")

def rank(request):
    return render(request, "rank.html")

def contest(request):
    return render(request, "contest/contest.html")

def register(request):
    return render(request, "user/register.html")

def login(request):
    return render(request, "user/login.html")

def problem(request, problem_id):
    return render(request, "problem/problem.html", {
       "problem_title": "问题标题"
    });

# contest
def contest_overview(request, contest_id):
    contest_title = "比赛标题"
    overview_text = "###欢迎参加XXX大赛\n本次大赛准备了丰厚的奖品  \n第一名可免费使用一年校园网\n\n祝大家比赛愉快~喵~\n\n<del>第二名可以免费用两年！</del>  \n![头像](https://avatars1.githubusercontent.com/u/7625230?s=100)"
    return render(request, "contest/contest-overview.html", {
        'contest_id': contest_id,
        'contest_title': contest_title,
        'overview_text': markdown(overview_text)
    })

def contest_problemset(request, contest_id):
    contest_title = "比赛标题"
    return render(request, "contest/contest-problemset.html", {
        'contest_id': contest_id,
        'contest_title': contest_title,
    })

def contest_ranklist(request, contest_id):
    contest_title = "比赛标题"
    return render(request, "contest/contest-ranklist.html", {
        'contest_id': contest_id,
        'contest_title': contest_title,
    })

def contest_statistics(request, contest_id):
    contest_title = "比赛标题"
    return render(request, "contest/contest-statistics.html", {
        'contest_id': contest_id,
        'contest_title': contest_title,
    })

def contest_status(request, contest_id):
    contest_title = "比赛标题"
    return render(request, "contest/contest-status.html", {
        'contest_id': contest_id,
        'contest_title': contest_title,
    })

@login_required(redirect_field_name='login', login_url=None)
def modify_user_info(request):
    username = request.user.username
    email = request.user.email
    school = request.user.school
    student_id = request.user.student_id
    gender = request.user.gender
    return render(request, "user/modify-user-info.html", {
        'username': username,
        'email': email,
        'school': school,
        'student_id': student_id,
        'gender': gender
    })

