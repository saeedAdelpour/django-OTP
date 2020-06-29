from django.core.exceptions import ValidationError, EmptyResultSet

form_phone_number = "phone"
form_otp_code = "code"
form_change_name = "new_name"
form_name = "name"
request_useragent = "HTTP_USER_AGENT"
request_token = "HTTP_AUTHORIZATION"


def number_valid(request):
  number = request.POST.get(form_phone_number)
  value_len = get_num_len(number)

  if not number:
    raise EmptyResultSet("no number got")
  elif value_len < 6:
    raise ValidationError("number is too short")
  elif value_len > 10:
    raise ValidationError("number out of range")
  return number


def useragent_valid(request):
  user_agent = request.META.get(request_useragent)
  if not user_agent:
    raise EmptyResultSet("empty user agent")
  return user_agent


def otp_valid(request):
  otp = request.POST.get(form_otp_code)
  value_len = get_num_len(otp)

  if not value_len:
    raise EmptyResultSet("empty otp")
  elif value_len > 4:
    raise ValidationError("otp out of range")
  return otp


def name_valid(request, form_label):
  name = request.POST.get(form_name)
  if is_int(name):
    raise ValidationError("enter string for name not number")
  if not name:
    raise EmptyResultSet("empty name")
  return name


def token_valid(request):
  token_header = request.META.get(request_token)
  if not token_header:
    raise EmptyResultSet("empty user token")


def get_num_len(num):
  return len(str(num))

def is_int(value):
  try:
    num = int(value)
  except:
    return False
  return True
