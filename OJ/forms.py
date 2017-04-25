from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=50)
    school = forms.CharField(max_length=20, required=False)
    student_id = forms.CharField(max_length=26, required=False)
    password = forms.CharField(max_length=128)
    confirm = forms.CharField(max_length=128)
    gender = forms.ChoiceField(choices=(('boy', '男孩子'), ('girl', '女孩子'), ('futa', '其他')))

class LogginForm(forms.Form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(max_length=128)

class ModifyUserInfoForm(forms.Form):
    username = forms.CharField(max_length=30, error_messages={'required':'用户名不能为空', 'invalid':'请输入正确的用户名'})
    about = forms.CharField(max_length=140, required=False, error_messages={'required':'个性签名不能为空', 'invalid':'请输入正确的个性签名'})
    school = forms.CharField(max_length=20, required=False, error_messages={'required':'学校不能为空', 'invalid':'请输入正确的学校'})
    student_id = forms.CharField(max_length=26, required=False, error_messages={'required':'学号不能为空', 'invalid':'请输入正确的学号'})
    password = forms.CharField(max_length=128, required=False, error_messages={'required':'密码不能为空', 'invalid':'请输入正确的密码'})
    new_password = forms.CharField(max_length=128, required=False, error_messages={'required':'新密码不能为空', 'invalid':'请输入正确的新密码'})
    confirm = forms.CharField(max_length=128, required=False, error_messages={'required':'确认密码不能为空', 'invalid':'请输入正确的确认'})
    gender = forms.ChoiceField(choices=(('boy', '男孩子'), ('girl', '女孩子'), ('futa', '其他')), error_messages={'required':'性别不能为空', 'invalid':'请输入正确的性别'})