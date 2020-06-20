from django.shortcuts import render
from django.http.response import JsonResponse
from random import random
from .models import Client, Session
from django.views.decorators.csrf import csrf_exempt
import jwt

form_phone_numebr = "phone"
form_otp_code = "code"

@csrf_exempt
def enter(request):
  number = request.POST.get(form_phone_numebr)
  user_agent = request.META.get("HTTP_USER_AGENT")

  # get client
  try:
    client = Client.objects.get(number=number)
    message = "got your account"
  except:
    client = Client(number=number)
    message = "create new account"
  
  client.set_otp()

  # get session
  try:
    session = Session.objects.get(client=client, user_agent=user_agent)
  except:
    session = Session(client=client , user_agent=user_agent)

  client.save()
  session.save()
  response = {"success": message}
  return JsonResponse(response)

key = 'my site is cool'
algorithm = "HS256"

@csrf_exempt
def verify(request):
  user_agent = request.META.get("HTTP_USER_AGENT")
  if not user_agent:
    return JsonResponse({"message": "empty user agent"})

  number = request.POST.get(form_phone_number)
  if not number:
    return JsonResponse({"message": "enter phone number"})

  otp = request.POST.get(form_otp_code)
  if not otp:
    return JsonResponse({"message": "enter code"})

  try:
    client = Client.objects.get(otp=otp, number=number)
    session = Session.objects.get(client=client, user_agent=user_agent)
  except:
    return JsonResponse({"message": "invalid data"})

    payload = {"id": session.id}
  token = jwt.encode(payload, key, algorithm).decode("utf-8")
    # client.set_none_otp()
    # client.save()
  
  return JsonResponse({"message": "success", "token": token})

@csrf_exempt
def create(request):
  token_header = request.META.get("HTTP_AUTHORIZATION")
  if not token_header:
    return JsonResponse({"message": "your token is empty"})

  token = token_header[7:]
  try:
    payload = jwt.decode(token, key, algorithm)
  except:
    return JsonResponse({"message": "invalid data form token got"})

  user_agent = request.META.get("HTTP_USER_AGENT")
  if not user_agent:
    return JsonResponse({"message": "user_agent is empty"})

      identity = payload.get("id")
      session = Session.objects.get(id=identity, user_agent=user_agent)
  client = session.client

  name = request.POST.get("name")
  if not name:
    return JsonResponse({"message": "your name is empty"})

      if not client.name:
        client.name = name
  else:
    message = "{}, can't change your name".format(client.name)
  
  client.login()
        client.save()
    
  return JsonResponse({"message": message})

@csrf_exempt
def change(request):

  # check token
  tolen_header = request.META.get("HTTP_AUTHORIZATION")
  if not tolen_header:
    return JsonResponse({"message": "empty token"})
        
  # check payload
  token = tolen_header[7:]
  try:
    payload = jwt.decode(token, key, algorithm)
    except:
    return JsonResponse({"message": "invalid token"})
  
  identity = payload.get("id")
  session = Session.objects.get(id=identity)
  client = session.client

  if not client.is_auth():
    return JsonResponse({"message": "login first"})
  
  new_name = request.POST.get(form_change_name)
  if not new_name:
    return JsonResponse({"message": "no name got"})

  message = "{}, you successfully change your name to {}".format(client.name, new_name)
  client.name = new_name
  client.save()

  return JsonResponse({"message": message})