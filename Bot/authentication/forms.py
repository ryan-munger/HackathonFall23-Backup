from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student

class StudentRegisterForm(UserCreationForm):
    GRADE_CHOICES = (
        ("college", "College"),
        ("highschool", "High School"),
        ("middle_school", "Middle School"),
    )
    grade = forms.ChoiceField(choices=GRADE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'grade')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        grade = self.cleaned_data['grade']
        # Create StudentProfile linked to the user
        student_profile = Student.objects.create(user=user, grade=grade)
        student_profile.save()
        return user
