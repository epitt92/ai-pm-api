from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password

import json

from .forms import UserRegisterationForm, UserLoginForm
from .models import User


# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):

        data = json.loads(request.body)
        form = UserRegisterationForm(data)

        if form.is_valid():
            email = data.get('email', None)
            password = make_password(data.get('password'))
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            date_of_birth = data.get('date_of_birth', None)
            biography = data.get('biography', '')
            profile_picture = data.get('profile_picture', '')
            wallet_address = data.get('wallet_address')
            role = data.get('role', '2')
            is_verified = data.get('is_verified', False)
            token_balance = data.get('token_balance', 0)

            user = User.objects(wallet_address=wallet_address).first()
            if user:
                return JsonResponse({'message': 'Already existed user'}, safe=False)
            else:
                user = User(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=date_of_birth,
                    biography=biography,
                    profile_picture=profile_picture,
                    wallet_address=wallet_address,
                    role=role,
                    is_verified=is_verified,
                    token_balance=token_balance
                ).save()

                return JsonResponse({'message': 'Created successfully'}, safe=True)

        else:
            return JsonResponse({'message': 'Invalid inputs', 'errors': form.errors}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class SigninView(View):
    def post(self, request):

        data = json.loads(request.body)
        form = UserLoginForm(data)

        if form.is_valid():
            password = data.get('password')
            wallet_address = data.get('wallet_address')
            role = data.get('role', '2')

            user = User.objects.filter(wallet_address=wallet_address).first()
            print(user.password)
            if user:
                if check_password(password, user.password):
                    request.session['user_id'] = str(user.id)
                    request.session['wallet_address'] = user.wallet_address
                    request.session['role'] = user.role

                    return JsonResponse({'message': 'Logged in successfully.'}, safe=True)

                else:
                    return JsonResponse({'message': 'Invalid password'}, safe=False)
            else:
                return JsonResponse({'message': 'Account is not existed'}, safe=False)

        else:
            return JsonResponse({'message': 'Invalid inputs', 'errors': form.errors}, safe=False)
