from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password, check_password

import json
import random

from .forms import UserRegisterationForm, UserLoginForm
from .models import User, Requester, Tasker
from utils import is_valid_solana_address, verify_signature


# Create your views here.


@method_decorator(csrf_exempt, name="dispatch")
class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        form = UserRegisterationForm(data)
        print("called")

        if form.is_valid():
            name = data.get("name", "")
            profile_picture = data.get("profile_picture", "")
            wallet_address = data.get("wallet_address")
            wallet_type = data.get("wallet_type")
            role = data.get("role", "tasker")  # ["tasker", "requester"]
            is_verified = data.get("is_verified", False)
            token_balance = data.get("token_balance", 0)

            if role != "2":
                user = Tasker.objects(
                    **{f"{wallet_type}Address": wallet_address}
                ).first()
            else:
                user = Requester.objects(
                    **{f"{wallet_type}Address": wallet_address}
                ).first()

            if user:
                return JsonResponse(
                    {"message": "Already existed user"}, safe=False, status=400
                )
            else:
                if role != "2":
                    user = Tasker(
                        name=name,
                        profile_picture=profile_picture,
                        **{f"{wallet_type}Address": wallet_address},
                        role=role,
                        is_verified=is_verified,
                        token_balance=token_balance,
                    ).save()
                else:
                    user = Requester(
                        name=name,
                        profile_picture=profile_picture,
                        **{f"{wallet_type}Address": wallet_address},
                        role=role,
                        is_verified=is_verified,
                        token_balance=token_balance,
                    ).save()

                return JsonResponse({"message": "Created successfully"}, safe=True)

        else:
            return JsonResponse(
                {"message": "Invalid inputs", "errors": form.errors},
                safe=False,
                status=400,
            )


@method_decorator(csrf_exempt, name="dispatch")
class SigninView(View):
    def post(self, request):
        data = json.loads(request.body)
        form = UserLoginForm(data)

        if form.is_valid():
            publicKey = data.get("publicKey")
            requestNonce = data.get("requestNonce")
            signature = data.get("signature")
            walletType = data.get("walletType")
            registerFlag = False

            if is_valid_solana_address(publicKey) == False:
                return JsonResponse(
                    {"message": "Invalid ${walletType} wallet address provided"},
                    safe=False,
                    status=400,
                )

            # Generate a nonce (random number) between 10000 and 109998
            nonce = str(random.randint(10000, 109998))

            requester = (
                Requester.objects.filter(solanaAddress=publicKey).first()
                or Requester.objects.filter(ethereumAddress=publicKey).first()
            )
            tasker = (
                Tasker.objects.filter(solanaAddress=publicKey).first()
                or Tasker.objects.filter(ethereumAddress=publicKey).first()
            )
            print("requester")
            print(requester)
            print(tasker)
            user = requester or tasker
            if user is None:
                registerFlag = True

            if requestNonce:
                if registerFlag:
                    request.session[publicKey] = nonce
                else:
                    user.nonce = nonce
                    user.save()

                return JsonResponse({"nonce": nonce}, safe=True, status=200)

            if registerFlag:
                nonceToVerify = request.session.get(publicKey)
            else:
                nonceToVerify = user.nonce

            verified = verify_signature(nonceToVerify, signature, publicKey, walletType)

            if verified == False:
                return JsonResponse(
                    {"message": "Invalid signature, unable to login"},
                    safe=False,
                    status=400,
                )

            print(registerFlag)
            print(requester)
            print(tasker)
            if registerFlag:
                user = Requester.objects.create(
                    **{f"{walletType}Address": publicKey},
                )
            else:
                user.nonce = nonce
                user.save()

            request.session["userId"] = str(user.id)
            request.session["role"] = "Requester" if requester else "Tasker"
            request.session["logged"] = True

            print("request.session")
            print(request.session["userId"])
            return JsonResponse(
                {"message": "Logged in successfully", "user": {"name": user.name, "role": request.session["role"]}},
                safe=True,
                status=200,
            )

        else:
            return JsonResponse(
                {"message": "Invalid inputs", "errors": form.errors},
                safe=False,
                status=400,
            )


def logout(request):
    if "logged" in request.session:
        del request.session["logged"]
        request.session.flush()  # Optional: Flush all of the session data
        return JsonResponse({"message": "You are logged out"}, safe=True, status=200)
    else:
        return JsonResponse(
            {"message": "You are already logged out"}, safe=False, status=400
        )
