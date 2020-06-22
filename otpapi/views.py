from django.shortcuts import render
from django.http.response import JsonResponse
from random import random
from .models import Client, Session
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import FieldDoesNotExist
from .token import Token

form_phone_number = "phone"
form_otp_code = "code"
form_change_name = "new_name"
  # TODO: validate number by regex
  # TODO: use custom exception classes and catch them in exception handler middleware

@csrf_exempt
def enter(request):
  user_agent = request.META.get("HTTP_USER_AGENT")
  if not user_agent:
    raise FieldDoesNotExist("empty user agent")

  number = request.POST.get(form_phone_number)
  if not number:
    raise FieldDoesNotExist("no number got")

  try:
    client = Client.objects.get(number=number)
  except:
    client = Client(number=number)
  
  client.set_new_otp()
  client.save()

  try:
    Session.objects.get(client=client, user_agent=user_agent)
  except:
    session = Session(client=client , user_agent=user_agent)
  session.save()

  return JsonResponse({"success": True})
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
  token = Token.get_token(payload=payload)
  # client.set_none_otp()
  # client.save()

  return JsonResponse({"message": "success", "token": token})

@csrf_exempt
def create(request):
  token_header = request.META.get("HTTP_AUTHORIZATION")
  if not token_header:
    return JsonResponse({"message": "your token is empty"})

  payload = Token.decode_token(token_header=token_header)

  user_agent = request.META.get("HTTP_USER_AGENT")
  if not user_agent:
    return JsonResponse({"message": "user_agent is empty"})

  identity = payload.get("id")
  session = Session.objects.get(id=identity, user_agent=user_agent)
  client = session.client

  if not client.name:
    name = request.POST.get("name")
    if not name:
      return JsonResponse({"message": "your name is empty"})
    client.name = name
    
  message = "{}, successfully logged in".format(client.name)
  
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
  payload = Token.decode_token(token_header=tolen_header)
  
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