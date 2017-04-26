from django.contrib import admin
from django.conf import settings
from OJ.models import *


# 管理后台主页
class MoeOJAdmin(admin.AdminSite):
    site_header = getattr(settings, 'OJ_TITLE', 'Moe Online Judge') + ' 设定'


admin_site = MoeOJAdmin()


# 用户
@admin.register(User, site=admin_site)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'password', 'created_at', 'school', 'student_id', 'gender',
              'user_type', 'submission_number', 'accepted_problem_number', 'about')
    readonly_fields = ('created_at', 'email')
    search_fields = ('username', 'email')

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
    list_display = ('title',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'supplemental', 'is_enable', 'judge_example')
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
