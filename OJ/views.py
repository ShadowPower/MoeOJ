from django.shortcuts import render
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
    return render(request, "register.html")

def login(request):
    return render(request, "login.html")

def problem(request, problem_id):
    return render(request, "problem/problem.html")

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