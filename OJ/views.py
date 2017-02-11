from django.shortcuts import render
from OJ.helper import Helper
from markdown import markdown

# Create your views here.
def index(request):
    return render(request, "index.html", {'background_class': Helper.get_background_class()})

def problemset(request):
    return render(request, "problemset.html", {'background_class': Helper.get_background_class()})

def status(request):
    return render(request, "status.html", {'background_class': Helper.get_background_class()})

def rank(request):
    return render(request, "rank.html", {'background_class': Helper.get_background_class()})

def contest(request):
    return render(request, "contest/contest.html", {'background_class': Helper.get_background_class()})

def register(request):
    return render(request, "register.html", {'background_class': Helper.get_background_class()})

def login(request):
    return render(request, "login.html", {'background_class': Helper.get_background_class()})

# contest
def contest_overview(request, contest_id):
    contest_title = "比赛标题"
    overview_text = "###欢迎参加XXX大赛\n本次大赛准备了丰厚的奖品  \n第一名可免费使用一年校园网\n\n祝大家比赛愉快~喵~\n\n<del>第二名可以免费用两年！</del>  \n![头像](https://avatars1.githubusercontent.com/u/7625230?s=100)"
    return render(request, "contest/contest-overview.html", {
        'background_class': Helper.get_background_class(),
        'contest_id': contest_id,
        'contest_title': contest_title,
        'overview_text': markdown(overview_text)
    })

def contest_problemset(request, contest_id):
    contest_title = "比赛标题"
    return render(request, "contest/contest-problemset.html", {
        'background_class': Helper.get_background_class(),
        'contest_id': contest_id,
        'contest_title': contest_title,
    })

def contest_ranklist(request, contest_id):
    contest_title = "比赛标题"
    return render(request, "contest/contest-ranklist.html", {
        'background_class': Helper.get_background_class(),
        'contest_id': contest_id,
        'contest_title': contest_title,
    })

def contest_statistics(request, contest_id):
    contest_title = "比赛标题"
    return render(request, "contest/contest-statistics.html", {
        'background_class': Helper.get_background_class(),
        'contest_id': contest_id,
        'contest_title': contest_title,
    })

def contest_status(request, contest_id):
    contest_title = "比赛标题"
    return render(request, "contest/contest-status.html", {
        'background_class': Helper.get_background_class(),
        'contest_id': contest_id,
        'contest_title': contest_title,
    })