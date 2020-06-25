from django.shortcuts import render
from django.http.response import JsonResponse
from random import random
from .models import Client, Session
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import EmptyResultSet
from .token import Token

form_phone_number = "phone"
form_otp_code = "code"
form_change_name = "new_name"

@csrf_exempt
def enter(request):
  user_agent = request.META.get("HTTP_USER_AGENT")
  if not user_agent:
    raise EmptyResultSet("empty user agent")

  number = request.POST.get(form_phone_number)
  if not number:
    raise EmptyResultSet("no number got")

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
    raise EmptyResultSet("empty user agent")

  number = request.POST.get(form_phone_number)
  if not number:
    raise EmptyResultSet("empty number")

  otp = request.POST.get(form_otp_code)
  if not otp:
    raise EmptyResultSet("empty otp")

  # TODO: fix getting session use client objects
  try:
    client = Client.objects.get(otp=otp, number=number)
    session = Session.objects.get(client=client, user_agent=user_agent)
  except:
    raise Client.DoesNotExist("client not found")

  payload = {"id": session.id}
  token = Token.get_token(payload=payload)
  # client.set_none_otp()
  # client.save()

  return JsonResponse({"success": True, "token": token})

@csrf_exempt
def create(request):
  token_header = request.META.get("HTTP_AUTHORIZATION")

  payload = Token.decode_token(token_header=token_header)

  user_agent = request.META.get("HTTP_USER_AGENT")
  if not user_agent:
    raise EmptyResultSet("empty user agent")

  identity = payload.get("id")
  session = Session.objects.get(id=identity, user_agent=user_agent)
  client = session.client

  if not client.name:
    name = request.POST.get("name")
    if not name:
      raise EmptyResultSet("empty name")
    client.name = name
    
  message = "{}, successfully logged in".format(client.name)
  
  client.login()
  client.save()
    
  return JsonResponse({"success": True})

@csrf_exempt
def change(request):
  tolen_header = request.META.get("HTTP_AUTHORIZATION")
  if not tolen_header:
    raise EmptyResultSet("empty user agent")

  payload = Token.decode_token(token_header=tolen_header)
  
  identity = payload.get("id")
  session = Session.objects.get(id=identity)
  client = session.client

  if not client.is_auth():
    raise Exception("login first")
  
  new_name = request.POST.get(form_change_name)
  if not new_name:
    raise EmptyResultSet("empty name")

  former_name = client.name
  client.name = new_name

  try:
    name_not_valid = int(new_name)
    raise Exception("fill digits not numebr")
  except ValueError as exception:
    pass

  client.save()
  message = "{former_name}, you successfully change your name to {new_name}".format(former_name=former_name, new_name=new_name)

  return JsonResponse({"message": message})