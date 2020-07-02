from django.shortcuts import render
from django.http.response import JsonResponse
from random import random
from .models import Client, Session
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import EmptyResultSet
from .token import Token
from .validators import number_valid, useragent_valid, otp_valid, name_valid, token_valid

@csrf_exempt
def enter(request):
  user_agent = useragent_valid(request)

  number = number_valid(request)

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
  user_agent = useragent_valid(request)

  number = number_valid(request)

  otp = otp_valid(request)

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
  token_header = token_valid(request)

  payload = Token.decode_token(token_header=token_header)

  user_agent = useragent_valid(request)

  identity = payload.get("id")
  session = Session.objects.get(id=identity, user_agent=user_agent)
  client = session.client

  if not client.name:
    name = name_valid(request)
    client.name = name
    
  message = "{}, successfully logged in".format(client.name)
  
  client.login()
  client.save()
    
  return JsonResponse({"success": True, "message": message})

@csrf_exempt
def change(request):
  token_header = token_valid(request)

  payload = Token.decode_token(token_header=token_header)
  
  identity = payload.get("id")
  session = Session.objects.get(id=identity)
  client = session.client

  if not client.is_auth():
    raise Exception("login first")
  
  new_name = name_valid(request)

  former_name = client.name
  client.name = new_name

  client.save()
  message = "{former_name}, you successfully change your name to {new_name}".format(former_name=former_name, new_name=new_name)

  return JsonResponse({"success": True, "message": message})