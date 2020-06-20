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
  otp = request.POST.get(form_otp_code)
  number = request.POST.get(form_phone_numebr)
  user_agent = request.META.get("HTTP_USER_AGENT")

  try:
    client = Client.objects.get(otp=otp, number=number)
    session = Session.objects.get(client=client)
    payload = {"id": session.id}
    token = jwt.encode(payload, key, algorithm).decode('utf-8')
    # client.set_none_otp()
    # client.save()
    message = "token created"
  except:
    token = None
    message = "invalid code. try again"

  
  response = {"message": message, "token": token}
  return JsonResponse(response)

@csrf_exempt
def create(request):
  token_header = request.META.get("HTTP_AUTHORIZATION")
  if not token_header:
    return JsonResponse({"message": "your token is empty"})

  token = token_header[7:]
  name = request.POST.get("name")
  user_agent = request.META.get("HTTP_USER_AGENT")

  payload = None
  try:
    payload = jwt.decode(token, key, algorithm)
    message = "token decoded"
  except:
    message = "your token is invalid"

  if payload:
    try:
      identity = payload.get("id")
      session = Session.objects.get(id=identity, user_agent=user_agent)
      client = Client.objects.get(id=session.client.id)
      message = "logged in"

      if not client.name:
        client.name = name
        client.save()
      else:
        message = "cant change name"
        
    except:
      message = "problem"

  response = {"message": message}
  return JsonResponse(response)