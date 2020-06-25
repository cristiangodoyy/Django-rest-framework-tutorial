from rest_framework import generics
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer, \
    SnippetSimpleSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly

"""
http http://127.0.0.1:8000/snippets/
http -a admin:adminadmin POST http://127.0.0.1:8000/snippets/ code="print(789)"

http http://127.0.0.1:8000/snippets/2/
http POST http://127.0.0.1:8000/snippets/ code="public class Name { }"
"""


class SnippetList(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    http://127.0.0.1:8008/snippets/
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSimpleSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSimpleSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
