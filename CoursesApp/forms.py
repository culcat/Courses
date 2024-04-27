from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, EducationalOrganization, Course


class CustomUserCreationForm(UserCreationForm):
    organization = forms.ModelChoiceField(queryset=EducationalOrganization.objects.all(), required=False)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'organization')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].choices = [choice for choice in self.fields['user_type'].choices if choice[0] in ['teacher', 'student']]

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class RatingForm(forms.Form):
    score = forms.IntegerField(min_value=0, max_value=10)
    position = forms.IntegerField(min_value=1)


from django import forms
from .models import Course
from .models import CustomUser

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'teacher', 'organization', 'max_score']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название курса'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Описание курса'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Образовательная организация'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Максимальный балл'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = CustomUser.objects.filter(user_type='teacher')
        self.fields['teacher'].initial = user  # Устанавливаем текущего пользователя по умолчанию для поля teacher
        # Получаем организацию текущего пользователя и устанавливаем её по умолчанию для поля organization
        if user.organization:
            self.fields['organization'].initial = user.organization