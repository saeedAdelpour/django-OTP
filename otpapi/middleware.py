from django.db.utils import DataError
from psycopg2.errors import NumericValueOutOfRange
from django.http.response import JsonResponse
from django.core.exceptions import FieldDoesNotExist
from .models import Client
from jwt.exceptions import InvalidSignatureError

class SimpleMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response
    # One-time configuration and initialization.

  def __call__(self, request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.

    # print("__call__: i am before get_response")
    response = self.get_response(request)
    # print("__call__: i am after get_response")

    # Code to be executed for each request/response after
    # the view is called.

    return response

  def process_view(self, request, view_func, view_args, view_kwargs):
    pass
    # print("process_view: in process_view")
  ValueError
  def process_exception(self, request, exception):
    exception_type = type(exception)
    
    exception_message = None
    if exception_type is DataError:
      exception_message = "out of range data"

    elif exception_type is FieldDoesNotExist:
      exception_message = str(exception)

    elif exception_type is ValueError:
      exception_message = "this data is invalid"

    elif exception_type is Client.DoesNotExist:
      exception_message = str(exception)

    elif exception_type is InvalidSignatureError:
      exception_message = "invalid token"
    
    return JsonResponse({"error_type": str(type(exception)), "error_message": exception_message})
