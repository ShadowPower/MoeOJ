from django.contrib import admin
from django.conf import settings
from OJ.models import *


# 管理后台主页
class MoeOJAdmin(admin.AdminSite):
    site_header = getattr(settings, 'OJ_TITLE', 'Moe Online Judge') + ' 控制面板'

admin_site = MoeOJAdmin()

# 公告
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')

# 题目
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin_site.register(Notice, NoticeAdmin)
admin_site.register(Problem, ProblemAdmin)