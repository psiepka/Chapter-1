from rest_framework import filters
from django.utils import timezone
from rest_framework import generics, permissions, renderers
from exams import models
from .serializers import (
    ExamSerializer, ExamDetailSerializer,
    ExamResultDetailSerializer, ExamTestSerializer, ExamTestAnswersSerializer,
    ExamResultsJudgeSerializer, ResultsListSerializer
)


class IsOwner(permissions.BasePermission):
    """
    Global permission check for user exam class, if user created that exam.
    """

    def has_object_permission(self, request, view, obj):
        return obj.examiner == request.user

class IsAvaiable(permissions.BasePermission):
    """
    Global permission check for user exam class, if user created that exam.
    """

    def has_object_permission(self, request, view, obj):
        return obj.avaiable or obj.examiner == request.user


class IsJudged(permissions.BasePermission):
    """
    Global permission check for user exam class, if user created that exam.
    """

    def has_object_permission(self, request, view, obj):
        return obj.judged or obj.examiner == request.user


class ExamList(generics.ListCreateAPIView):
    """
    List all exams
    """
    queryset = models.Exam.objects.filter(archivized=False)
    serializer_class = ExamSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = (
        'examiner', 'title', 'topic', 'created_in','avaiable', 'answered',
        'checking', 'judged', 'archivized', 'archivized_in'
    )
    ordering = ('-created_in',)

    def perform_create(self, serializer):
        serializer.save(examiner=self.request.user)


class ListResults(generics.ListAPIView):
    serializer_class = ResultsListSerializer
    queryset = models.Result.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('exam', 'student', 'grade')
    ordering = ('exam',)

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        queryset = models.Result.objects.all()
        username = self.kwargs.get('username', None)
        if username is not None:
            queryset = queryset.filter(student__username=username)
        return queryset

class ExamArchivesList(generics.ListAPIView):
    """
    List all exams
    """
    queryset = models.Exam.objects.filter(archivized=True)
    serializer_class = ExamSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = (
        'examiner', 'title', 'topic', 'created_in', 'answered',
        'judged', 'archivized', 'archivized_in'
    )
    ordering = ('-archivized_in',)


class ExamDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a exam instance.
    """
    queryset = models.Exam.objects.all()
    serializer_class = ExamDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.archivized:
            obj.archivized = True
            obj.archivized_in = timezone.now()
            obj.save()
        else:
            obj.delete
        return obj


class ExamResult(generics.RetrieveAPIView):
    """
    Retrieve, update or delete a exam instance.
    """
    queryset = models.Exam.objects.all()
    serializer_class = ExamResultDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsJudged)


class ResultOfExam(generics.RetrieveUpdateAPIView):
    serializer_class = ExamResultsJudgeSerializer
    queryset = models.Exam.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class ExamTest(generics.RetrieveUpdateAPIView):
    serializer_class = ExamTestSerializer
    queryset = models.Exam.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAvaiable)



class AssesmentAnswer(generics.RetrieveUpdateAPIView):
    queryset = models.Exam.objects.all()
    serializer_class = ExamTestAnswersSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
