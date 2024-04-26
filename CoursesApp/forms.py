from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, EducationalOrganization

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