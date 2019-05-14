from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.text import capfirst
from django import forms


class CommonLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': "Email",
            'class': 'form-control',
            'autofocus': 'autofocus',
            'required': 'required',
            'type': 'email'
        })
    )
    password = forms.CharField(
        label="Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "Password",
            'class': 'form-control',
            'required': 'required',
            'type': 'password'
        }),
    )

    error_messages = {
        'invalid_login': "Please enter a correct %(email)s and password. Note that both "
                         "fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # noinspection PyProtectedMember
        self.email_field = get_user_model()._meta.get_field(get_user_model().EMAIL_FIELD)
        self.fields['email'].max_length = self.email_field.max_length or 254
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.email_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            try:
                username = get_user_model().objects.get(email=email).username
            except get_user_model().DoesNotExist:
                raise self.get_invalid_login_error()
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.email_field.verbose_name},
        )


class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")
        field_classes = {'username': UsernameField, 'email': forms.EmailField}
