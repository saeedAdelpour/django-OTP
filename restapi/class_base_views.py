from rest_framework.views import APIView
from .models import Snippet
from .serializers import SnippetSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
      return self.create(request, *args, **kwargs)


  def get(self, request, pk, format=None):
    snippet = self.get_object(pk)
    serializer = SnippetSerializer(snippet)
    return Response(serializer.data)

  def put(self, request, pk, format=None):
    snippet = self.get_object(pk)
    serializer = SnippetSerializer(snippet, data=request.data)
    if serializer.is_valid():
      return Response(serializer.data)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    snippet = self.get_object(pk)
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
