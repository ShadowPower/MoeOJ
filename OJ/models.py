from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.utils.timezone import now
from django.dispatch import receiver

import os

# 用户权限
REGULAR_USER = 0
ADMIN = 1
SUPER_ADMIN = 2

USER_TYPE_CHOICES = (
    (REGULAR_USER, '普通用户'),
    (ADMIN, '管理员'),
    (SUPER_ADMIN, '超级管理员')
)

# 比赛状态
CONTEST_NOT_START = 0
CONTEST_UNDERWAY = 1
CONTEST_ENDED = 2

# 比赛类型
PUBLIC_CONTEST = 0
PRIVATE_CONTEST = 1

CONTEST_TYPE_CHOICES = (
    (PUBLIC_CONTEST, '公开'),
    (PRIVATE_CONTEST, '非公开')
)

# 运行结果
AC = 0  # Accepted
CE = 1  # Compile Error
WA = 2  # Wrong Answer
RE = 3  # Runtime Error
TLE = 4  # Time Limit Exceeded
OLE = 5  # Output Limit Exceeded
MLE = 6  # Memory Limit Exceeded
RF = 7  # Restricted Function
PE = 8  # Presentation Error

RESULT_CHOICES = (
    (AC, '答案正确'),
    (CE, '编译错误'),
    (WA, '答案错误'),
    (RE, '运行错误'),
    (TLE, '时间超限'),
    (OLE, '输出超限'),
    (MLE, '内存超限'),
    (RF, '函数受限'),
    (PE, '格式错误')
)

# 语言
LANG_C = 0
LANG_CPP = 1
LANG_JAVA = 2
LANG_PYTHON = 3

LANGUAGE_CHOICES = (
    (LANG_C, 'C'),
    (LANG_CPP, 'C++'),
    (LANG_JAVA, 'Java'),
    (LANG_PYTHON, 'Python')
)

GENDER_CHOICES = (
    ('boy', '男孩子'),
    ('girl', '女孩子'),
    ('futa', '其他')
)

DIFFICULTY_CHOICES = (
    (0, '入门'),
    (1, '简单'),
    (2, '中等'),
    (3, '困难'),
)


# 题目测试用例上传路径
def test_case_upload_path_handler(instance, filename):
    return "testcase/{file}".format(file=str(instance.id) + ".zip")


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.zip']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None, school=None, student_id=None, gender='boy'):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=name,
            email=UserManager.normalize_email(email),
            school=school,
            student_id=student_id,
            gender=gender
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name='超级管理员', school=None, student_id=None, gender='boy'):
        user = self.create_user(name, email, password, school, student_id, gender)
        user.user_type = SUPER_ADMIN
        user.save(using=self._db)
        return user


# 用户表
class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    # 用户名
    username = models.CharField('用户名', max_length=30)
    # 用户邮箱
    email = models.EmailField('E-mail', max_length=50, unique=True)
    # 用户类型
    user_type = models.IntegerField('权限级别', default=0, choices=USER_TYPE_CHOICES)
    # 学校
    school = models.CharField('学校', max_length=20, null=True, blank=True)
    # 学号
    student_id = models.CharField('学号', max_length=26, null=True, blank=True)
    # 性别
    gender = models.CharField('性别', max_length=5, default='boy', choices=GENDER_CHOICES)
    # 邮箱验证Token
    email_token = models.CharField('邮箱验证令牌', max_length=64, null=True, blank=True)
    # 注册时间
    created_at = models.DateTimeField('注册时间', auto_now_add=True, null=True, blank=True)
    # 总提交数（相同题目不可以重复统计）
    submission_number = models.IntegerField('总提交数', default=0)
    # 总AC数（相同题目不可以重复统计）
    accepted_problem_number = models.IntegerField('总AC数', default=0)
    # 个性签名
    about = models.TextField('个性签名', default='穿哪件衣服写代码好呢~', max_length=140, null=True, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        if self.user_type == SUPER_ADMIN or self.user_type == ADMIN:
            return True
        return False

    def has_module_perms(self, app_label):
        return True

    # 是否允许访问管理后台
    @property
    def is_staff(self):
        if self.user_type == SUPER_ADMIN or self.user_type == ADMIN:
            return True
        else:
            return False

    # 是否拥有管理后台的各种权限
    @property
    def is_superuser(self):
        if self.user_type == SUPER_ADMIN or self.user_type == ADMIN:
            return True
        else:
            return False

    def __str__(self):
        return self.username + ' [' + self.email + ']'


# 公告表
class Notice(models.Model):
    # 标题
    title = models.CharField('标题', max_length=30)
    # 作者
    author = models.ForeignKey(User, verbose_name='作者')
    # 日期时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 正文
    body = models.TextField('正文', null=True, blank=True)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'

    def __str__(self):
        return self.title


# 题目标签表
class ProblemTag(models.Model):
    name = models.CharField('标签', max_length=30)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


# 题目抽象表
class AbstractProblem(models.Model):
    # 题目标题
    title = models.CharField('标题', max_length=200)
    # 题目描述
    description = models.TextField('题目描述', null=True, blank=True)
    # 输入说明
    input_desc = models.TextField('输入描述', null=True, blank=True)
    # 输出说明
    output_desc = models.TextField('输出描述', null=True, blank=True)
    # 样例输入
    sample_input = models.TextField('样例输入', null=True, blank=True)
    # 样例输出
    sample_output = models.TextField('样例输出', null=True, blank=True)
    # 是否特判
    spj = models.BooleanField('是否为特殊判题题目（使用代码判题）', default=False)
    # 特判代码
    spj_code = models.TextField('特判代码', null=True, blank=True)
    # 补充说明
    supplemental = models.TextField('补充说明', null=True, blank=True)
    # 题目创建者
    created_by = models.ForeignKey(User, verbose_name='创建者', null=True, blank=True)
    # 添加时间
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # 时间限制
    time_limit = models.IntegerField('时间限制（毫秒）')
    # 内存限制
    memory_limit = models.IntegerField('内存限制（KB）')
    # 是否启用
    is_enable = models.BooleanField('在题目列表显示', default=True)
    # 总AC数
    accepted = models.IntegerField('总AC数', default=0, null=True, blank=True)
    # 总提交数
    submit = models.IntegerField('总提交数', default=0, null=True, blank=True)
    # 输入输出样例文件
    judge_example = models.FileField('样例文件（ZIP压缩包）', null=True, blank=True,
                                     upload_to=test_case_upload_path_handler, validators=[validate_file_extension])

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


# 题目表
class Problem(AbstractProblem):
    # 题目来源
    source = models.CharField('来源', max_length=30, null=True, blank=True)
    # 题目标签
    tags = models.ManyToManyField(ProblemTag, verbose_name='标签')
    # 题目难度 ( 0 ~ n )
    difficulty = models.IntegerField('难度', choices=DIFFICULTY_CHOICES)

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目'


# 比赛表
class Contest(models.Model):
    # 比赛标题
    title = models.CharField('标题', max_length=255)
    # 描述
    description = models.TextField('描述')
    # 开始时间
    start_time = models.DateTimeField('开始时间')
    # 结束时间
    end_time = models.DateTimeField('结束时间')
    # 创建时间
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    # 是否实时排名
    real_time_rank = models.BooleanField('开启实时排名')
    # 比赛类型（公开、私有）
    contest_type = models.IntegerField('类型', default=PUBLIC_CONTEST, choices=CONTEST_TYPE_CHOICES)
    # 比赛密码
    password = models.CharField('密码', max_length=30, blank=True, null=True)
    # 创建者
    created_by = models.ForeignKey(User, verbose_name='比赛创建者')
    # 是否可见
    visible = models.BooleanField('是否在比赛列表显示', default=True)
    # 非公开比赛参赛选手
    contestant = models.ManyToManyField(User, verbose_name='参赛选手（用于非公开比赛）', related_name='contestants', blank=True)

    @property
    def status(self):
        if self.start_time > now():
            # 没有开始 返回0
            return CONTEST_NOT_START
        elif self.end_time < now():
            # 已经结束 返回2
            return CONTEST_ENDED
        else:
            # 正在进行 返回1
            return CONTEST_UNDERWAY

    class Meta:
        verbose_name = '比赛'
        verbose_name_plural = '比赛'

    def __str__(self):
        return self.title


# 比赛题目表
class ContestProblem(AbstractProblem):
    # 题目所属比赛
    contest = models.ForeignKey(Contest, verbose_name='所属比赛')
    # 题目序号，用于排序，例如：0 1 2 3 4
    index = models.IntegerField('题目序号（从0开始，不能跳跃）', default=0)

    class Meta:
        verbose_name = '比赛题目'
        verbose_name_plural = '比赛题目'


# 比赛排名表
class ContestRank(models.Model):
    # 用户
    user = models.ForeignKey(User, verbose_name='用户')
    # 比赛
    contest = models.ForeignKey(Contest, verbose_name='比赛', db_index=True)
    # 总提交
    submit = models.IntegerField('总提交', default=0)
    # 总AC
    accepted = models.IntegerField('总AC', default=0)
    # 总耗时
    total_time = models.IntegerField('总耗时', default=0)

    class Meta:
        verbose_name = '比赛排名'
        verbose_name_plural = '比赛排名'

    def __str__(self):
        return '用户：' + self.user.username + ' 比赛：' + self.contest.title


# 比赛题目成绩表
class ContestResult(models.Model):
    '''
    用来存放比赛中对应题目的成绩
    记录每一题的耗时（从比赛开始到第一次AC的时间）
    和罚时（AC之前答案错误的次数）
    当答案错误时，如果没有耗时记录，则罚时+1
    当AC时，如果没有耗时记录，则记录耗时
    如果存在耗时记录，此数据不再变更
    '''
    # 用户
    user = models.ForeignKey(User, verbose_name='用户', db_index=True)
    # 比赛
    contest = models.ForeignKey(Contest, verbose_name='比赛', db_index=True)
    # 题目
    problem = models.ForeignKey(ContestProblem, verbose_name='题目', db_index=True)
    # 罚时
    penalty = models.IntegerField('罚时', default=0)
    # 首次AC时间
    ac_time = models.DateTimeField('首次AC时间', null=True, blank=True)


# 提交记录抽象表
class AbstractSolution(models.Model):
    # 用户
    user = models.ForeignKey(User, db_index=True, verbose_name='用户')
    # 使用时间（毫秒）
    time = models.IntegerField('运行耗时（毫秒）', default=0)
    # 使用内存（KB）
    memory = models.IntegerField('消耗内存（KB）', default=0)
    # 提交时间
    submit_date = models.DateTimeField('提交时间', auto_now_add=True)
    # 判题开始时间
    judge_start_time = models.DateTimeField('判题开始时间', blank=True, null=True)
    # 判题结束时间
    judge_end_time = models.DateTimeField('判题结束时间', blank=True, null=True)
    # 语言 0:C 1:C++ 2:Java 3:Python
    language = models.IntegerField('语言', default=0, choices=LANGUAGE_CHOICES)
    # 评判结果
    result = models.SmallIntegerField('判题结果', null=True, blank=True, choices=RESULT_CHOICES)
    # 用户IP
    ip = models.CharField('用户IP', max_length=46, null=True, blank=True)
    # 代码
    code = models.TextField('代码')
    # 判题结果，例如编译错误信息，运行错误信息
    info = models.TextField('附加信息', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username


# 提交记录表
class Solution(AbstractSolution):
    # 对应问题
    problem = models.ForeignKey(Problem, db_index=True, verbose_name='题目')

    class Meta:
        verbose_name = '提交记录'
        verbose_name_plural = '提交记录'


# 比赛提交记录表
class ContestSolution(AbstractSolution):
    # 对应比赛，空值表示非比赛题目
    contest = models.ForeignKey(Contest, db_index=True, verbose_name='所属比赛')
    # 对应比赛问题
    problem = models.ForeignKey(ContestProblem, db_index=True, verbose_name='比赛题目')

    class Meta:
        verbose_name = '比赛提交记录'
        verbose_name_plural = '比赛提交记录'


# 评论
class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name='用户')
    problem = models.ForeignKey(Problem, verbose_name='题目', db_index=True)
    date = models.DateTimeField('评论日期', auto_now_add=True)
    body = models.TextField('正文', null=True, blank=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return self.author.username + ' | ' + self.problem.title + ' | ' + self.date.strftime('%Y-%m-%d %H:%M:%S')


# 题目删除之后，删除判题用例文件
@receiver(models.signals.post_delete, sender=Problem)
@receiver(models.signals.post_delete, sender=ContestProblem)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.judge_example:
        try:
            if os.path.isfile(instance.judge_example.path):
                os.remove(instance.judge_example.path)
        except Exception:
            return False


# 题目修改之前，删除已经存在的判题用例文件
@receiver(models.signals.pre_save, sender=Problem)
def auto_delete_testcase_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Problem.objects.get(pk=instance.pk).judge_example
    except Problem.DoesNotExist:
        return False

    new_file = instance.judge_example
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except ValueError:
            return False


# 比赛题目修改之前，删除已经存在的判题用例文件
@receiver(models.signals.pre_save, sender=ContestProblem)
def auto_delete_contest_testcase_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = ContestProblem.objects.get(pk=instance.pk).judge_example
    except Problem.DoesNotExist:
        return False

    new_file = instance.judge_example
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except ValueError:
            return False