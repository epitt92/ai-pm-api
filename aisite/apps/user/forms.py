from django import forms

role_choices = (
    ("1", "Administrator"),
    ("2", "Normal")
)


class UserRegisterationForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)
    biography = forms.CharField(required=False)
    profile_picture = forms.CharField(required=False)
    wallet_address = forms.CharField(required=True)
    role = forms.ChoiceField(choices=role_choices, required=True)
    is_verified = forms.BooleanField(required=False)
    token_balance = forms.IntegerField(required=False)


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField(required=True)
    wallet_address = forms.CharField(required=True)
