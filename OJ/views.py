from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q

from OJ.models import *

from markdown import markdown
import codecs

OBJECTS_PER_PAGE = 25

# Create your views here.
def index(request):
    notices = Notice.objects.all().order_by("-created_at")
    return render(request, "index.html", {'notices': notices, 'markdown': markdown})

def problemset(request):
    rank_list = User.objects.filter(submission_number__gt=0).order_by("-accepted_problem_number", "-submission_number")[:15]
    tag_list = ProblemTag.objects.all()
    problem_list = Problem.objects.filter(is_enable=True)
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

    return render(request, "problem/problemset.html", {
        "page": problems,
        "pages": pages,
        "rank_list": rank_list,
        "tags": tag_list
    })

# 题目搜索
def problem_search(request):
    key_text = request.GET.get('key')
    tag_text = request.GET.get('tag')
    problem_list = Problem.objects.filter(is_enable=True)
    if key_text is not None:
        problem_list = problem_list.filter(title__contains=key_text)
    if tag_text is not None:
        problem_list = problem_list.filter(tags__name=tag_text)
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

    return render(request, "problem/problemsearch.html", {
        "page": problems,
        "pages": pages,
    })

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
    contest_list = Contest.objects.filter(visible=True)
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
    problem_object = Problem.objects.get(id=problem_id)
    return render(request, "problem/problem-description.html", {
        'problem': problem_object,
        'is_contest': False
    })

def problem_status(request, problem_id):
    problem_object = Problem.objects.get(id=problem_id)
    solution_list = Solution.objects.filter(problem_id=problem_id)
    submit_count = solution_list.count()

    # 取得各结果的统计
    statistics = Solution.objects.values('result').filter(problem_id=problem_id).annotate(count=Count('result'))
    result_count = [0] * 9
    for i in statistics:
        result_count[i['result']] = i['count']

    paginator = Paginator(solution_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    try:
        solution = paginator.page(page_number)
    except PageNotAnInteger:
        solution = paginator.page(1)
    except EmptyPage:
        solution = paginator.page(paginator.num_pages)
    pages = paginator.num_pages
    return render(request, "problem/problem-status.html", {
        'problem': problem_object,
        'page': solution,
        'pages': pages,
        'submit_count': submit_count,
        'result_count':result_count,
        'is_contest': False
    })

# contest
def contest_overview(request, contest_id):
    contest_object = Contest.objects.get(id=contest_id)
    overview_text = contest_object.description
    return render(request, "contest/contest-overview.html", {
        'contest': contest_object,
        'overview_text': markdown(overview_text)
    })

def contest_problemset(request, contest_id):
    contest_object = Contest.objects.get(id=contest_id)
    # 题目列表
    contest_problem_list = ContestProblem.objects.filter(contest_id=contest_id, is_enable=True).order_by("index")
    # 各题目AC数量
    accepted_count = [0] * contest_problem_list.count()
    # 查询本比赛，本用户的提交记录中所有AC的记录，然后Group By题目id，统计数量（AC次数）
    if request.user.is_authenticated():
        statistics = ContestSolution.objects.values('problem__index')\
            .filter(contest_id=contest_id, problem__is_enable=True, user=request.user, result=0)\
            .annotate(count=Count('problem'))
        # 记录AC次数到accepted_count数组中
        for i in statistics:
            accepted_count[i['problem__index']] = i['count']

    return render(request, "contest/contest-problemset.html", {
        'contest': contest_object,
        'problem_list': contest_problem_list,
        'accepted_count': accepted_count
    })

def contest_problem(request, problem_id):
    problem_object = ContestProblem.objects.get(id=problem_id)
    return render(request, "problem/problem-description.html", {
        'problem': problem_object,
        'is_contest': True
    })

def contest_problem_status(request, problem_id):
    problem_object = ContestProblem.objects.get(id=problem_id)
    solution_list = ContestSolution.objects.filter(problem_id=problem_id)
    submit_count = solution_list.count()

    # 取得各结果的统计
    statistics = ContestSolution.objects.values('result').filter(problem_id=problem_id).annotate(count=Count('result'))
    result_count = [0] * 9
    for i in statistics:
        result_count[i['result']] = i['count']

    paginator = Paginator(solution_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    try:
        solution = paginator.page(page_number)
    except PageNotAnInteger:
        solution = paginator.page(1)
    except EmptyPage:
        solution = paginator.page(paginator.num_pages)
    pages = paginator.num_pages
    return render(request, "problem/problem-status.html", {
        'problem': problem_object,
        'page': solution,
        'pages': pages,
        'submit_count': submit_count,
        'result_count':result_count,
        'is_contest': True
    })

def contest_ranklist(request, contest_id):
    contest_object = Contest.objects.get(id=contest_id)
    return render(request, "contest/contest-ranklist.html", {
        'contest': contest_object,
    })

def contest_statistics(request, contest_id):
    contest_object = Contest.objects.get(id=contest_id)
    # 取得各结果的统计
    # 取得题目数量
    problem_count = ContestProblem.objects.filter(contest_id=contest_id).count()
    # data[题号 p_index][结果类型 result] = 数量
    data = [[0] * 9] * problem_count
    # select count(ContestSolution.result) ...... group by Problem.index ContestSolution.result
    statistics = ContestSolution.objects.filter(contest_id=contest_id).values('problem__index', 'result')\
        .annotate(count=Count('result'))
    # 写入二维数组
    for i in statistics:
        data[i['problem__index']][i['result']] = i['count']
    return render(request, "contest/contest-statistics.html", {
        'contest': contest_object,
        'data': data
    })

def contest_status(request, contest_id):
    contest_object = Contest.objects.get(id=contest_id)
    solution_list = ContestSolution.objects.filter(contest_id=contest_id)
    paginator = Paginator(solution_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    try:
        solution = paginator.page(page_number)
    except PageNotAnInteger:
        solution = paginator.page(1)
    except EmptyPage:
        solution = paginator.page(paginator.num_pages)
    pages = paginator.num_pages

    return render(request, "contest/contest-status.html", {
        'contest': contest_object,
        'page': solution,
        'pages': pages
    })

@login_required(redirect_field_name='login', login_url=None)
def modify_user_info(request):
    user = request.user
    return render(request, "user/modify-user-info.html", {
        'user': user
    })

