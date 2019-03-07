"""
All views classes for exams feature
"""

from rest_framework import filters
from django.utils import timezone
from rest_framework import (
    generics, permissions, response, status
)
from exams import models
from .serializers import (
    ExamSerializer, ExamDetailSerializer,
    ExamResultDetailSerializer, ExamTestSerializer, ExamTestAnswersSerializer,
    ExamResultsJudgeSerializer, ResultsListSerializer
)


class IsOwner(permissions.BasePermission):
    """
    Global permission check for user exam class,
    Check if user created that exam.
    """

    def has_object_permission(self, request, view, obj):
        return obj.examiner == request.user

class IsAvaiable(permissions.BasePermission):
    """
    Global permission check for user exam class
    Check if exam is set to avaiable to student.
    """

    def has_object_permission(self, request, view, obj):
        return obj.avaiable or obj.examiner == request.user


class IsJudged(permissions.BasePermission):
    """
    Global permission check for user exam class
    Check that all tests of exam are judged
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
        'examiner', 'title', 'topic', 'created_in', 'avaiable', 'answered',
        'checking', 'judged', 'archivized', 'archivized_in'
    )
    ordering = ('-created_in',)

    def perform_create(self, serializer):
        serializer.save(examiner=self.request.user, created_in=timezone.now())


class ListResults(generics.ListAPIView):
    """
    List all results of exam model
    """

    serializer_class = ResultsListSerializer
    queryset = models.Result.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('exam', 'student', 'grade')
    ordering = ('exam',)

    def get_queryset(self):
        """
        This view return a list of all the results for
        the user as determined by the username of the URL.
        """
        queryset = models.Result.objects.all()
        username = self.kwargs.get('username', None)
        if username is not None:
            queryset = queryset.filter(student__username=username)
        return queryset


class ExamArchivesList(generics.ListAPIView):
    """
    List all exams archives.
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
            obj.delete()
        return response.Response(status=status.HTTP_200_OK)


class ExamResult(generics.RetrieveAPIView):
    """
    Retrieve exam instance.
    Private view result of exam student
    """
    queryset = models.Exam.objects.all()
    serializer_class = ExamResultDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsJudged)


class ResultOfExam(generics.RetrieveUpdateAPIView):
    """
    View for examiner with all tests of exam
    """

    serializer_class = ExamResultsJudgeSerializer
    queryset = models.Exam.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class ExamTest(generics.RetrieveUpdateAPIView):
    """
    View of page where we create and update Answers for questions of exam
    """

    serializer_class = ExamTestSerializer
    queryset = models.Exam.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAvaiable)


class AssesmentAnswer(generics.RetrieveUpdateAPIView):
    """
    View for examiner, where examiner can create of update assesments of answers of exam
    """

    queryset = models.Exam.objects.all()
    serializer_class = ExamTestAnswersSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
