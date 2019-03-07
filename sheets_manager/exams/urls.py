from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from exams import views

urlpatterns = [
    path('', views.ExamList.as_view(), name='exam-list'),
    path('results/', views.ListResults.as_view(), name='results-list'),
    re_path(r'^results/user=(?P<username>.+)/$', views.ListResults.as_view(), name='results-list-query'),
    path('archives/', views.ExamArchivesList.as_view(), name='exam-list'),
    path('<int:pk>/', views.ExamDetail.as_view(), name='exam-detail'),
    path('<int:pk>/result/', views.ExamResult.as_view(), name='exam-result'),
    path('<int:pk>/results/', views.ResultOfExam.as_view(), name='exam-judge-results'),
    path('<int:pk>/test/', views.ExamTest.as_view(), name='exam-test'),
    path('<int:pk>/assesment/', views.AssesmentAnswer.as_view(), name='exam-assesment'),
]

urlpatterns = format_suffix_patterns(urlpatterns)