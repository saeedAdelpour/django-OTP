from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from .models import Account
import random

def createAccount(request):
  context = {}
  if request.method == "POST":
    phone_number = request.POST.get("phone_number")
    if phone_number:
      otp_number = random.random() * 10 ** 4
      try:
        account = Account.objects.get(phone_number=phone_number)
      except:
        account = Account(otp_number=otp_number, phone_number=phone_number)
      account.save()
      return redirect('verification')
  return render(request, 'otpverify/account_form.html', context)

def verify(request):
  if request.method == "POST":
    otp_number = request.POST.get("otp_number")
    try:
      account = Account.objects.get(otp_number=otp_number)
      url = 'create/?phone_number=' + str(account.phone_number)
      return redirect(url)
    except:
      return render(request, 'otpverify/verify.html', {"error": "not correct"})
  return render(request, 'otpverify/verify.html')

def create(request):
  phone_number = request.GET.get("phone_number")
  if request.method == "POST":
    account = Account.objects.get(phone_number=phone_number)
    account.name = request.POST.get('name')
    account.save()
    return redirect('home')
  return render(request, 'otpverify/create.html')

def getOtp(request):
  phone_number = request.GET.get('phone_number')
  try:
    account = Account.objects.get(phone_number=phone_number)
    response = {
      "otp": account.otp_number
    }
    status = 200
  except:
    response = {
      "error": "this phone number not found"
    }
    status = 404

  return JsonResponse(response, status=status)