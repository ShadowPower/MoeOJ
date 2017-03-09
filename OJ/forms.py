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