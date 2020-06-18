from django.core.validators import ValidationError

def signValidate(value):
  if "@" not in value:
    raise ValidationError("not have @")
  return value

def saeedValidate(value):
  if "saeed" not in value:
    raise ValidationError("not have saeed")
  return value