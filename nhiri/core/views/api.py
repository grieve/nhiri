from rest_framework import generics
from rest_framework import permissions

from nhiri.core import models
from nhiri.core import serializers


class MomentList(generics.ListCreateAPIView):
    model = models.Moment
    serializers = serializers.MomentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CaffeineMomentList(generics.ListCreateAPIView):
    model = models.CaffeineMoment
    serializers = serializers.CaffeineMomentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
