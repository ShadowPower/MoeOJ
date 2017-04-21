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

oj_urls = [
    url(r'^problem/(\d+)/$', oj_views.problem, name='problem'),
    url(r'^problem-status/(\d+)/$', oj_views.problem_status, name='problem-status'),
    url(r'^problemset/$', oj_views.problemset, name='problemset'),
    url(r'^status/$', oj_views.status, name='status'),
    url(r'^rank/$', oj_views.rank, name='rank'),
    url(r'^contest/$', oj_views.contest, name='contest'),
    url(r'^contest/overview/(\d+)/$', oj_views.contest_overview, name='contest_overview'),
    url(r'^contest/problemset/(\d+)/$', oj_views.contest_problemset, name='contest_problemset'),
    url(r'^contest/ranklist/(\d+)/$', oj_views.contest_ranklist, name='contest_ranklist'),
    url(r'^contest/statistics/(\d+)/$', oj_views.contest_statistics, name='contest_statistics'),
    url(r'^contest/status/(\d+)/$', oj_views.contest_status, name='contest_status'),
    url(r'^register/$', oj_views.register, name='register'),
    url(r'^login/$', oj_views.login, name='login'),
    url(r'^modify-user-info/$', oj_views.modify_user_info, name='modify-user-info'),
]

oj_form_urls = [
    url(r'^register-post/$', oj_form_views.register_post, name='register-post'),
    url(r'^login-post/$', oj_form_views.login_post, name='login-post'),
    url(r'^logout/$', oj_form_views.logout_get, name='logout'),
]

urlpatterns = [
    url(r'^$', oj_views.index, name='index'),
    url(r'', include(oj_urls)),
    url(r'', include(oj_form_urls)),
    url(r'^admin/', admin.site.urls, name='admin'),
]
