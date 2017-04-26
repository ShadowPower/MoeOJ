"""MoeOJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from OJ import views as oj_views
from OJ import form_views as oj_form_views
from OJ import admin_views as admin_views
from OJ.admin import admin_site

oj_urls = [
    url(r'^problem/(\d+)/$', oj_views.problem, name='problem'),
    url(r'^problem-search/$', oj_views.problem_search, name='problem_search'),
    url(r'^problem-status/(\d+)/$', oj_views.problem_status, name='problem_status'),
    url(r'^problemset/$', oj_views.problemset, name='problemset'),
    url(r'^status/$', oj_views.status, name='status'),
    url(r'^rank/$', oj_views.rank, name='rank'),
    url(r'^register/$', oj_views.register, name='register'),
    url(r'^login/$', oj_views.login, name='login'),
    url(r'^modify-user-info/$', oj_views.modify_user_info, name='modify_user_info'),
]

contest_urls = [
    url(r'^$', oj_views.contest, name='contest'),
    url(r'^overview/(\d+)/$', oj_views.contest_overview, name='contest_overview'),
    url(r'^problemset/(\d+)/$', oj_views.contest_problemset, name='contest_problemset'),
    url(r'^problem/(\d+)/$', oj_views.contest_problem, name='contest_problem'),
    url(r'^problem-status/(\d+)/$', oj_views.contest_problem_status, name='contest_problem_status'),
    url(r'^ranklist/(\d+)/$', oj_views.contest_ranklist, name='contest_ranklist'),
    url(r'^statistics/(\d+)/$', oj_views.contest_statistics, name='contest_statistics'),
    url(r'^status/(\d+)/$', oj_views.contest_status, name='contest_status'),
]

oj_form_urls = [
    url(r'^register-post/$', oj_form_views.register_post, name='register_post'),
    url(r'^login-post/$', oj_form_views.login_post, name='login_post'),
    url(r'^logout/$', oj_form_views.logout_get, name='logout'),
    url(r'^modify-user-info-post/', oj_form_views.modify_user_info_post, name='modify_user_info_post'),
]

urlpatterns = [
    url(r'^$', oj_views.index, name='index'),
    url(r'', include(oj_urls)),
    url(r'', include(oj_form_urls)),
    url(r'^contest/', include(contest_urls)),
    url(r'^admin/', admin_site.urls, name='admin'),
]
