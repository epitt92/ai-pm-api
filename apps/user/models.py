from mongoengine import *

# Create your models here.


class User(Document):
    meta = {'collection': 'users'}
    email = EmailField(
        verbose_name='Email Address', required=False)
    password = StringField(required=False)
    first_name = StringField(max_length=30, verbose_name='First Name')
    last_name = StringField(max_length=30, verbose_name='Last Name')
    date_of_birth = DateTimeField(verbose_name='Date of Birth')
    biography = StringField(verbose_name='Biography')
    profile_picture = StringField(verbose_name='Profile Picture')
    solanaAddress = StringField(
        max_length=100, verbose_name='Address')
    ethereumAddress = StringField(
        max_length=100, verbose_name='Address')
    nonce = StringField(max_length=30, verbose_name='Nonce', required=False)
    role = StringField(max_length=20, verbose_name='Role')
    is_verified = BooleanField(default=False, verbose_name='Is Verified')
    token_balance = DecimalField(precision=10, verbose_name='Token Balance')
    created_at = DateTimeField()
    updated_at = DateTimeField()
    deleted_at = DateTimeField()
