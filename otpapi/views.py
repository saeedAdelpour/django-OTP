from django.shortcuts import render
from django.http.response import JsonResponse
from random import random
from .models import Client
from django.views.decorators.csrf import csrf_exempt
import jwt

@csrf_exempt
def enter(request):
  phone = request.POST.get("phone")

  try:
    client = Client.objects.get(number=phone)
    message = "got your account"
  except:
    client = Client(number=phone)
    message = "create new account"
  
  client.set_otp()

  client.save()
  response = {"success": message}
  return JsonResponse(response)

key = 'my site is cool'
algorithm = "HS256"

@csrf_exempt
def verify(request):
  otp = request.POST.get("code")

  try:
    client = Client.objects.get(otp=otp)
    payload = {"id": client.id}
    token = jwt.encode(payload, key, algorithm).decode('utf-8')
    message = "hello"
  except:
    message = "not valid code"

  response = {"message": message, "token": token}
  return JsonResponse(response)

@csrf_exempt
def create(request):
  token = request.META['HTTP_AUTHORIZATION'][7:]
  name = request.POST.get("name")

  try:
    payload = jwt.decode(token, key, algorithm)
    message = "token decoded"
  except:
    message = "token decode failed"

  if payload:
    try:
      identity = payload.get("id")
      client = Client.objects.get(id=identity)

      if not client.name:
        client.name = name
        client.save()
      else:
        message = "cant change name"
        
      message = "logged in"
    except:
      message = "problem"

  response = {"message": message}
  return JsonResponse(response)