from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password

import json
import random

from .forms import UserRegisterationForm, UserLoginForm
from .models import User
from utils import is_valid_solana_address, verify_signature


# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):

        data = json.loads(request.body)
        form = UserRegisterationForm(data)

        if form.is_valid():
            email = data.get('email', None)
            if data.get('password'):
                password = make_password(data.get('password'))
            else:
                password = None
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
                return JsonResponse({'message': 'Already existed user'}, safe=False, status=400)
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
            return JsonResponse({'message': 'Invalid inputs', 'errors': form.errors}, safe=False, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class SigninView(View):
    def get(self, request):
        print(request.session.get('wallet'))
        if (request.session.get('wallet') == None):
            request.session['wallet'] = 'apple wallet'
        return JsonResponse({'message': ''})

    def post(self, request):
        data = json.loads(request.body)
        form = UserLoginForm(data)

        if form.is_valid():
            publicKey = data.get('publicKey')
            requestNonce = data.get('requestNonce')
            signature = data.get('signature')
            walletType = data.get('walletType')
            registerFlag = False
            nonceToVerify = None

            if is_valid_solana_address(publicKey) == False:
                return JsonResponse({'message': 'Invalid ${walletType} wallet address provided'}, safe=False, status=400)

            # Generate a nonce (random number) between 10000 and 109998
            nonce = str(random.randint(10000, 109998))

            user = User.objects.filter(solanaAddress=publicKey).first() or User.objects.filter(
                ethereumAddress=publicKey).first()
            if user is None:
                registerFlag = True

            if requestNonce:
                if registerFlag:
                    request.session[publicKey] = nonce
                else:
                    user.nonce = nonce
                    user.save()

                return JsonResponse({'nonce': nonce}, safe=True, status=200)

            if registerFlag:
                nonceToVerify = request.session.get(publicKey)
            else:
                nonceToVerify = user.nonce

            verified = verify_signature(
                nonceToVerify, signature, publicKey, walletType)

            if verified == False:
                return JsonResponse({'message': 'Invalid signature, unable to login'}, safe=False, status=400)

            if registerFlag:
                user = User.objects.create(
                    **{f'{walletType}Address': publicKey},
                )
            else:
                user.nonce = nonce
                user.save()

            request.session['userId'] = str(user.id)
            request.session['logged'] = True

            return JsonResponse({'message': 'Logged in successfully'}, safe=True, status=200)

        else:
            return JsonResponse({'message': 'Invalid inputs', 'errors': form.errors}, safe=False, status=400)


def logout(request):
    if 'logged' in request.session:
        del request.session['logged']
        request.session.flush()  # Optional: Flush all of the session data
        return JsonResponse({'message': 'You are logged out'}, safe=True, status=200)
    else:
        return JsonResponse({'message': 'You are already logged out'}, safe=False, status=400)
