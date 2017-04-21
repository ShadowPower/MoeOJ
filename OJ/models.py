from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.utils.timezone import now

# 用户权限
REGULAR_USER = 0
ADMIN = 1
SUPER_ADMIN = 2

# 比赛状态
CONTEST_NOT_START = 0
CONTEST_UNDERWAY = 1
CONTEST_ENDED = 2

# 比赛类型
PUBLIC_CONTEST = 0
PRIVATE_CONTEST = 1

# 运行结果
AC = 0    # Accepted
CE = 1    # Compile Error
WA = 2    # Wrong Answer
RE = 3    # Runtime Error
TLE = 4   # Time Limit Exceeded
OLE = 5   # Output Limit Exceeded
MLE = 6   # Memory Limit Exceeded
RF = 7    # Restricted Function
PE = 8    # Presentation Error

# 语言
LANG_C = 0
LANG_CPP = 1
LANG_JAVA = 2
LANG_PYTHON = 3

class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None, school=None, student_id=None, gender='boy'):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = name,
            email = UserManager.normalize_email(email),
            school = school,
            student_id = student_id,
            gender = gender
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_super_user(self, name, email, password=None, school=None, student_id=None, gender='boy'):
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
    username = models.CharField(max_length=30)
    # 用户邮箱
    email = models.EmailField(max_length=50, unique=True)
    # 用户类型
    user_type = models.IntegerField(default=0)
    # 学校
    school = models.CharField(max_length=20, null=True)
    # 学号
    student_id = models.CharField(max_length=26, null=True)
    # 性别
    gender = models.CharField(max_length=5, default='boy')
    # 邮箱验证Token
    email_token = models.CharField(max_length=64, null=True)
    # 注册时间
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # 总提交数（相同题目不可以重复统计）
    submission_number = models.IntegerField(default=0)
    # 总AC数（相同题目不可以重复统计）
    accepted_problem_number = models.IntegerField(default=0)
    # 个性签名
    about = models.TextField(max_length=140, null=True)

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        if self.user_type == SUPER_ADMIN:
            return True
        if self.user_type == ADMIN and perm == 'admin':
            return True
        return False

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.user_type == SUPER_ADMIN:
            return True
        else:
            return False


# 公告表
class Notice(models.Model):
    # 标题
    title = models.CharField(max_length=30)
    # 作者
    author = models.ForeignKey(User)
    # 日期时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 正文
    body = models.TextField(null=True)

# 题目标签表
class ProblemTag(models.Model):
    name = models.CharField(max_length=30)

# 题目抽象表
class AbstractProblem(models.Model):
    # 题目标题
    title = models.CharField(max_length=200)
    # 题目描述
    description = models.TextField(null=True)
    # 输入说明
    input_desc = models.TextField(null=True)
    # 输出说明
    output_desc = models.TextField(null=True)
    # 样例输入
    sample_input = models.TextField(null=True)
    # 样例输出
    sample_output = models.TextField(null=True)
    # 是否特判
    spj = models.BooleanField(default=False)
    # 特判代码
    spj_code = models.TextField(null=True)
    # 补充说明
    supplemental = models.TextField(null=True)
    # 题目创建者
    created_by = models.ForeignKey(User)
    # 添加时间
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    # 时间限制
    time_limit = models.IntegerField()
    # 内存限制
    memory_limit = models.IntegerField()
    # 是否启用
    is_enable = models.BooleanField(default=True)
    # 总AC数
    accepted = models.IntegerField(default=0, null=True)
    # 总提交数
    submit = models.IntegerField(default=0, null=True)

    class Meta:
        abstract = True

# 题目表
class Problem(AbstractProblem):
    # 题目来源
    source = models.CharField(max_length=30, null=True)
    # 题目标签
    tags = models.ManyToManyField(ProblemTag)
    # 题目难度 ( 0 ~ n )
    difficulty = models.IntegerField()

# 比赛表
class Contest(models.Model):
    # 比赛标题
    title = models.CharField(max_length= 255)
    # 描述
    description = models.TextField()
    # 开始时间
    start_time = models.DateTimeField()
    # 结束时间
    end_time = models.DateTimeField()
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 是否实时排名
    real_time_rank = models.BooleanField()
    # 比赛密码
    password = models.CharField(max_length=30, blank=True, null=True)
    # 比赛类型（公开、私有）
    contest_type = models.IntegerField(default=PUBLIC_CONTEST)
    # 创建者
    created_by = models.ForeignKey(User)
    # 是否可见
    visible = models.BooleanField(default=True)

    @property
    def status(self):
        if self.start_time > now():
            # 没有开始 返回1
            return CONTEST_NOT_START
        elif self.end_time < now():
            # 已经结束 返回-1
            return CONTEST_ENDED
        else:
            # 正在进行 返回0
            return CONTEST_UNDERWAY

# 比赛题目表
class ContestProblem(AbstractProblem):
    # 题目所属比赛
    contest = models.ForeignKey(Contest)
    # 题目序号，用于排序，例如：A B C D E
    index = models.CharField(max_length=30)
    # 是否已经公开
    is_public = models.BooleanField(default=False)

# 比赛排名表
class ContestRank(models.Model):
    # 用户
    user = models.ForeignKey(User)
    # 比赛
    contest = models.ForeignKey(Contest)
    # 总提交
    submit = models.IntegerField(default=0)
    # 总AC
    accepted = models.IntegerField(default=0)
    # 总耗时
    total_time = models.IntegerField(default=0)

# 提交记录抽象表
class AbstractSolution(models.Model):
    # 用户
    user = models.ForeignKey(User, db_index=True)
    # 使用时间（毫秒）
    time = models.IntegerField(default=0)
    # 使用内存（KB）
    memory = models.IntegerField(default=0)
    # 提交时间
    submit_date = models.DateTimeField(auto_now_add=True)
    # 判题开始时间
    judge_start_time = models.BigIntegerField(blank=True, null=True)
    # 判题结束时间
    judge_end_time = models.BigIntegerField(blank=True, null=True)
    # 语言 0:C 1:C++ 2:Java 3:Python
    language = models.IntegerField(default=0)
    # 评判结果
    result = models.SmallIntegerField(null=True)
    # 用户IP
    ip = models.CharField(max_length=46, null=True)
    # 代码
    code = models.TextField()
    # 判题结果，例如编译错误信息，运行错误信息
    info = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

# 提交记录表
class Solution(AbstractSolution):
    # 对应问题
    problem = models.ForeignKey(Problem, db_index=True)

# 比赛提交记录表
class ContestSolution(AbstractSolution):
    # 对应比赛，空值表示非比赛题目
    contest = models.ForeignKey(Contest, db_index=True)
    # 对应比赛问题
    problem = models.ForeignKey(ContestProblem, db_index=True)


# 评论
class Comment(models.Model):
    author = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(null=True)
