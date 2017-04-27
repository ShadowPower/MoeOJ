from django.contrib import admin
from django.conf import settings
from django.forms.models import BaseInlineFormSet
from OJ.models import *


# 管理后台主页
class MoeOJAdmin(admin.AdminSite):
    site_header = getattr(settings, 'OJ_TITLE', 'Moe Online Judge') + ' 控制面板'
    site_title = site_header


admin_site = MoeOJAdmin()


# 重判提交记录
def rejudge(modeladmin, request, queryset):
    pass


rejudge.short_description = '重判所选的 提交'


# 用户
@admin.register(User, site=admin_site)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'password', 'created_at', 'school', 'student_id', 'gender',
              'user_type', 'submission_number', 'accepted_problem_number', 'about')
    readonly_fields = ('created_at', 'email')
    search_fields = ('username', 'email')
    list_display = ('username', 'email', 'school', 'student_id', 'gender', 'created_at', 'about')

    def save_model(self, request, obj, form, change):
        new_password = form.cleaned_data['password']
        if len(new_password) > 0 and new_password[:6] != 'pbkdf2':
            obj.set_password(new_password)
        obj.save()

    # 如果不是超级管理员，则全部只读
    def get_readonly_fields(self, request, obj=None):
        if not request.user.user_type == SUPER_ADMIN:
            return self.fields
        else:
            return self.readonly_fields

    def get_fields(self, request, obj=None):
        if not request.user.user_type == SUPER_ADMIN:
            return ('username', 'email', 'created_at', 'school', 'student_id', 'gender',
                    'user_type', 'submission_number', 'accepted_problem_number', 'about')
        else:
            return self.fields


# 公告
@admin.register(Notice, site=admin_site)
class NoticeAdmin(admin.ModelAdmin):
    fields = ('title', 'body')
    list_display = ('title', 'body')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


# 标签
@admin.register(ProblemTag, site=admin_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


# 题目
@admin.register(Problem, site=admin_site)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_enable', 'source', 'difficulty', 'time_limit', 'memory_limit', 'accepted', 'submit')
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'supplemental', 'is_enable', 'judge_example', 'source',
                       'tags', 'difficulty')
        }),
        ('输入和输出', {
            'fields': ('input_desc', 'output_desc', 'sample_input', 'sample_output')
        }),
        ('限制', {
            'fields': ('time_limit', 'memory_limit')
        }),
        ('高级选项', {
            'classes': ('collapse',),
            'fields': ('spj', 'spj_code')
        }),
        ('特殊选项', {
            'classes': ('collapse',),
            'fields': ('accepted', 'submit')
        })
    )

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


# 提交记录
@admin.register(Solution, site=admin_site)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'memory', 'submit_date', 'language', 'result', 'ip', 'problem')
    actions = (rejudge,)


# 比赛题目
class ContestProblemInline(admin.StackedInline):
    model = ContestProblem
    min_num = 0
    max_num = 256
    extra = 0
    list_display = ('title',)
    fieldsets = (
        ('基本信息', {
            'classes': ('collapse',),
            'fields': ('title', 'description', 'supplemental', 'is_enable', 'judge_example', 'contest', 'index')
        }),
        ('输入和输出', {
            'classes': ('collapse',),
            'fields': ('input_desc', 'output_desc', 'sample_input', 'sample_output')
        }),
        ('限制', {
            'classes': ('collapse',),
            'fields': ('time_limit', 'memory_limit')
        }),
        ('高级选项', {
            'classes': ('collapse',),
            'fields': ('spj', 'spj_code')
        }),
        ('特殊选项', {
            'classes': ('collapse',),
            'fields': ('accepted', 'submit')
        })
    )


# 比赛
@admin.register(Contest, site=admin_site)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'real_time_rank', 'contest_type', 'password', 'visible')
    inlines = (ContestProblemInline,)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    # 提交表单
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        # 如有标记删除则删除
        for obj in formset.deleted_objects:
            obj.delete()
        # 如果没有created by，则写入当前登录用户
        for instance in instances:
            if formset.model == ContestProblem and not instance.created_by:
                instance.created_by = request.user
            instance.save()
        formset.save_m2m()


# 比赛排名
@admin.register(ContestRank, site=admin_site)
class ContestRankAdmin(admin.ModelAdmin):
    list_display = ('user', 'contest', 'submit', 'accepted', 'total_time')


# 比赛提交记录
@admin.register(ContestSolution, site=admin_site)
class ContestSolutionAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'memory', 'submit_date', 'language', 'result', 'ip', 'contest', 'problem')
    actions = (rejudge,)


# 评论
@admin.register(Comment, site=admin_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'problem', 'date', 'body')
