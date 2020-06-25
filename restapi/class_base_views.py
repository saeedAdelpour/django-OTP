from rest_framework.views import APIView
from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions, renderers
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import action

class SnippetHighlight(generics.GenericAPIView):
  queryset = Snippet.objects.all()
  renderer_classes = [renderers.StaticHTMLRenderer]

  def get(self, request, *args, **kwargs):
    snippet = self.get_object()
    return Response(snippet.highlighted)


class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
      return self.create(request, *args, **kwargs)
  
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
  
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

  def get(self, request, *args, **kwargs):
    return super().retrieve(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    return super().update(request, *args, **kwargs)

  def delete(self, request, *args, **kwargs):
    return super().destroy(request, *args, **kwargs)


class SnippetViewSet(viewsets.ModelViewSet):
  """
  This viewset automatically provides `list`, `create`, `retrieve`,
  `update` and `destroy` actions.

  Additionally we also provide an extra `highlight` action.
  """
  
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

  @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
  def highlight(self, request, *args, **kwargs):
    snippet = self.get_object()
    return Response(snippet.highlighted)

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
  """
  This viewset automatically provides `list` and `detail` actions.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer