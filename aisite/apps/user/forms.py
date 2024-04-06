from django import forms

role_choices = (
    ("1", "Administrator"),
    ("2", "Normal")
)

walletType_choices = (
    ("solana", "solana"),
    ("ethereum", "ethereum")
)


class UserRegisterationForm(forms.Form):
    name = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=False)
    biography = forms.CharField(required=False)
    profile_picture = forms.CharField(required=False)
    wallet_address = forms.CharField(required=True)
    wallet_type = forms.CharField(required=True)
    role = forms.ChoiceField(choices=role_choices, required=True)
    is_verified = forms.BooleanField(required=False)
    token_balance = forms.IntegerField(required=False)


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField(required=False)
    requestNonce = forms.CharField(required=True)
    publicKey = forms.CharField(required=True)
    walletType = forms.ChoiceField(choices=walletType_choices, required=True)
    signature = forms.CharField(required=False)
