from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action

from ..models import Course, Subject

from . import serializers
from .permissions import IsEnrolled


class SubjectReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для модели Subject.
    Позволяет `retrieve()`, 'list()' действия.
    """
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = [permissions.AllowAny]


class CourseReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для модели Course.
    Добавлен метод 'enroll()' для записи на курс.
    Добавлен метод 'content()' для получения всего контента курса.
    """
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer

    @action(detail=True,
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        """
        Метод зачисляет студентов на курсы.
        """
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @action(detail=True,
            methods=['get'],
            serializer_class=serializers.CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        """
        Метод возвращает данные курса, его модули и содержимое.
        """
        return self.retrieve(request, *args, **kwargs)
