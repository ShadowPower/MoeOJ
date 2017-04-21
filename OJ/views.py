from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from OJ.models import *
from utils.helper import Helper

from markdown import markdown

OBJECTS_PER_PAGE = 25

# Create your views here.
def index(request):
    notices = Notice.objects.all().order_by("-created_at")
    return render(request, "index.html", {'notices': notices})

def problemset(request):
    gets_url = Helper.get_GETS_except(request, 'page')
    rank_list = User.objects.filter(submission_number__gt=0).order_by("-accepted_problem_number", "-submission_number")[:15]
    problem_list = Problem.objects.all()
    paginator = Paginator(problem_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    try:
        problems = paginator.page(page_number)
    except PageNotAnInteger:
        problems = paginator.page(1)
    except EmptyPage:
        problems = paginator.page(paginator.num_pages)
    pages = paginator.num_pages

    for problem in problems.object_list:
        # 计算AC比例
        try:
            problem.acrate = problem.accepted / problem.submit * 100
        except ZeroDivisionError:
            problem.acrate = 0

    return render(request, "problem/problemset.html", {"page": problems, "pages": pages, "gets": gets_url, "rank_list":rank_list})

def status(request):
    solution_list = Solution.objects.all()
    paginator = Paginator(solution_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    try:
        solution = paginator.page(page_number)
    except PageNotAnInteger:
        solution = paginator.page(1)
    except EmptyPage:
        solution = paginator.page(paginator.num_pages)
    pages = paginator.num_pages

    return render(request, "status.html", {"page": solution, "pages":pages})

def rank(request):
    rank_list = User.objects.filter(submission_number__gt=0).order_by("-accepted_problem_number", "-submission_number")
    paginator = Paginator(rank_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    try:
        ranks = paginator.page(page_number)
    except PageNotAnInteger:
        ranks = paginator.page(1)
    except EmptyPage:
        ranks = paginator.page(paginator.num_pages)
    pages = paginator.num_pages
    return render(request, "rank.html", {"page": ranks, "pages":pages, "objects_per_page": OBJECTS_PER_PAGE})

def contest(request):
    contest_list = Contest.objects.all().filter(visible=True)
    paginator = Paginator(contest_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    try:
        contests = paginator.page(page_number)
    except PageNotAnInteger:
        contests = paginator.page(1)
    except EmptyPage:
        contests = paginator.page(paginator.num_pages)
    pages = paginator.num_pages
    return render(request, "contest/contest.html", {"page": contests, "pages":pages})

def register(request):
    return render(request, "user/register.html")

def login(request):
    return render(request, "user/login.html")

def problem(request, problem_id):
    problemObject = Problem.objects.get(id=problem_id)
    return render(request, "problem/problem-description.html", {
        'problem': problemObject
    })

def problem_status(request, problem_id):
    problemObject = Problem.objects.get(id=problem_id)
    return render(request, "problem/problem-status.html", {
        'problem': problemObject
    })

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

