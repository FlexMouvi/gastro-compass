from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Review, TourReview, Booking
import re

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=20,
        required=False,
        label="Номер телефона (+7)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'})
    )
    email = forms.EmailField(
        required=True,
        label="Электронная почта",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            digits = re.sub(r'\D', '', phone)
            if len(digits) < 10:
                raise forms.ValidationError("Номер телефона должен содержать не менее 10 цифр.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data['phone']
            profile.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя или email',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя или email'
        self.fields['password'].label = 'Пароль'

class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Оценка'
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Ваш отзыв...'}),
        }

class TourReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Оценка'
    )

    class Meta:
        model = TourReview
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Ваш отзыв...'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'phone', 'email', 'date', 'guests', 'comment']  # добавили email
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),  # новое
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
            'comment': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Пожелания...'}),
        }