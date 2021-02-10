from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView

from ..models import Course, Subject

from . import serializers
from .permissions import IsEnrolled


class SubjectListView(generics.ListAPIView):
    """
    Обработчик списка предметов.
    """
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    """
    Обработчик подробностей предмето.
    """
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer


class CourseEnrollView(APIView):
    """
    Обработчик записи на курс.
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Набор обработчиков для модели Course.
    """
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer

    @action(detail=True,
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        """Метод зачисляет студентов на курсы."""
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @action(detail=True,
            methods=['get'],
            serializer_class=serializers.CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        """Метод возвращает данные курса, его модули и содержимое."""
        return self.retrieve(request, *args, **kwargs)
