from django import forms

from .models import User


class UserRegisterationForm(forms.Form):
    class Meta:
        email = forms.EmailField(required=False)
        pasword = forms.PasswordInput(required=True)

    #     model = User
    #     fields = ['email', 'password', 'first_name', 'last_name', 'date_of_birth', 'biography', 'profile_picture',
    #               'solana_address', 'ethereum_address', 'role', 'is_verified', 'token_balance']
    #     widgets = {
    #         'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
    #         'biography': forms.Textarea(attrs={'rows': 3}),
    #         'password': forms.PasswordInput(attrs={'minlenght': 8}),
    #         'profile_picture': forms.FileInput(),
    #     }
    #     # Specify required fields
    #     required = {
    #         'email': True,
    #         'password': True,
    #         'first_name': True,
    #         'last_name': True,
    #         'date_of_birth': False,  # Optional field
    #         'biography': False,      # Optional field
    #         'profile_picture': False,  # Optional field
    #         'solana_address': False,  # Optional field
    #         'ethereum_address': False,  # Optional field
    #         'role': False,           # Optional field
    #         'is_verified': False,    # Optional field
    #         'token_balance': False,  # Optional field
    #     }

    # def __init__(self, *args, **kwargs):
    #     super(UserRegisterationForm, self).__init__(*args, **kwargs)
    #     for field_name, is_required in self.Meta.required.items():
    #         self.fields[field_name].required = is_required


class UserLoginForm(forms.Form):
    class Meta:
        email = forms.EmailField(required=False)
        pasword = forms.PasswordInput(required=True)

    #     model = User
    #     fields = ['email', 'wallet_address', 'password']
    #     widgets = {
    #         'password': forms.PasswordInput(attrs={'minlenght': 8}),
    #     }
    #     # Specify required fields
    #     required = {
    #         'email': False,
    #         'password': True,
    #         'wallet_address': True,
    #     }

    # def __init__(self, *args, **kwargs):
    #     super(UserLoginForm, self).__init__(*args, **kwargs)
    #     for field_name, is_required in self.Meta.required.items():
    #         self.fields[field_name].required = is_required
