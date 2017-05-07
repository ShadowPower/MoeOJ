from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from OJ.models import *
from OJ.tasks import *

from markdown import markdown

OBJECTS_PER_PAGE = 25


# 创建分页
def make_pagination(queryset, request):
    paginator = Paginator(queryset, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.page(1)
    except EmptyPage:
        page_objects = paginator.page(paginator.num_pages)
    num_pages = paginator.num_pages
    return page_objects, num_pages


def index(request):
    notices = Notice.objects.all().order_by("-created_at")
    return render(request, "index.html", {'notices': notices, 'markdown': markdown})


def problemset(request):
    rank_list = User.objects.filter(submission_number__gt=0).order_by("-accepted_problem_number", "-submission_number")[
                :15]
    tag_list = ProblemTag.objects.all()
    problem_list = Problem.objects.filter(is_enable=True)
    problems, num_pages = make_pagination(problem_list, request)
    for problem in problems.object_list:
        # 计算AC比例
        try:
            problem.acrate = problem.accepted / problem.submit * 100
        except ZeroDivisionError:
            problem.acrate = 0

    return render(request, "problem/problemset.html", {
        "page": problems,
        "num_pages": num_pages,
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
    problems, num_pages = make_pagination(problem_list, request)

    for problem in problems.object_list:
        # 计算AC比例
        try:
            problem.acrate = problem.accepted / problem.submit * 100
        except ZeroDivisionError:
            problem.acrate = 0

    return render(request, "problem/problemsearch.html", {
        "page": problems,
        "num_pages": num_pages,
    })


def status(request):
    solution_list = Solution.objects.all().order_by("-submit_date")

    # 如果指定用户，则过滤结果
    user_id = request.GET.get('user')
    if user_id is not None:
        solution_list = solution_list.filter(user_id=user_id)

    solution, num_pages = make_pagination(solution_list, request)
    return render(request, "status.html", {"page": solution, "num_pages": num_pages})


def rank(request):
    rank_list = User.objects.filter(submission_number__gt=0).order_by("-accepted_problem_number", "-submission_number")
    ranks, num_pages = make_pagination(rank_list, request)
    return render(request, "rank.html", {"page": ranks, "num_pages": num_pages, "objects_per_page": OBJECTS_PER_PAGE})


def contest(request):
    contest_list = Contest.objects.filter(visible=True)
    contests, num_pages = make_pagination(contest_list, request)
    return render(request, "contest/contest.html", {"page": contests, "num_pages": num_pages})


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
    solution_list = Solution.objects.filter(problem_id=problem_id).order_by("-submit_date")
    submit_count = solution_list.count()

    # 如果指定用户，则过滤结果
    user_id = request.GET.get('user')
    if user_id is not None:
        solution_list = solution_list.filter(user_id=user_id)
        submit_count = solution_list.count()

    # 取得各结果的统计
    if user_id is None:
        statistics = Solution.objects.values('result').filter(problem_id=problem_id).annotate(count=Count('result'))
    else:
        statistics = Solution.objects.values('result').filter(problem_id=problem_id, user_id=user_id).annotate(count=Count('result'))

    result_count = [0] * 9
    for i in statistics:
        result_count[i['result']] = i['count']
    solutions, num_pages = make_pagination(solution_list, request)
    return render(request, "problem/problem-status.html", {
        'problem': problem_object,
        'page': solutions,
        'num_pages': num_pages,
        'submit_count': submit_count,
        'result_count': result_count,
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
        statistics = ContestSolution.objects.values('problem__index') \
            .filter(contest_id=contest_id, problem__is_enable=True, user=request.user, result=0) \
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
    solution_list = ContestSolution.objects.filter(problem_id=problem_id).order_by("-submit_date")
    submit_count = solution_list.count()

    # 取得各结果的统计
    statistics = ContestSolution.objects.values('result').filter(problem_id=problem_id).annotate(count=Count('result'))
    result_count = [0] * 9
    for i in statistics:
        result_count[i['result']] = i['count']

    solutions, num_pages = make_pagination(solution_list, request)
    return render(request, "problem/problem-status.html", {
        'problem': problem_object,
        'page': solutions,
        'num_pages': num_pages,
        'submit_count': submit_count,
        'result_count': result_count,
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
    statistics = ContestSolution.objects.filter(contest_id=contest_id).values('problem__index', 'result') \
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
    solution_list = ContestSolution.objects.filter(contest_id=contest_id).order_by("-submit_date")
    solutions, num_pages = make_pagination(solution_list, request)
    return render(request, "contest/contest-status.html", {
        'contest': contest_object,
        'page': solutions,
        'num_pages': num_pages
    })


@login_required(redirect_field_name='login', login_url=None)
def modify_user_info(request):
    user = request.user
    return render(request, "user/modify-user-info.html", {
        'user': user
    })

def user_info(request, user_id):
    user = User.objects.get(id=user_id)
    accepted_problem = Problem.objects.filter(solution__user_id=user_id, solution__result=AC).order_by('id')
    return render(request, "user/user-info.html", {
        'the_user': user,
        'accepted_problem': accepted_problem
    })
