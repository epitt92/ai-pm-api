from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from .forms import UserRegisterationForm, UserLoginForm

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            return JsonResponse({'valied': 'json response'})
        else:
            return JsonResponse({'valied': 'invalid'})
