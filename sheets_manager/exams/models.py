from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator


def validate_positive(value):
    """Function of int or float field validation.
    
    Arguments:
        value {int oor flaot} -- number which will be validate
    
    Raises:
        ValidationError -- when valeu is less than 0
    """
    if value < 0:
        raise ValidationError(
            _(f'{value} is not an positive number'),
            params={'value': value},
        )


class Exam(models.Model):
    """Class of exams feature.
    Arguments:
        requrired:
            examiner {User class} -- ForeignKey
            title {str} - max lenght:500, unique value
            topic {str} - max lenght:100
        optional:
            avaiable {bool} - (default: False) Boolean value that exam is avvaiable for students
            created_in {datatime} - (default: when created) Boolean value that exam is avvaiable for students
            created_in {datatime} - (default: when created) Boolean value that exam is avvaiable for students
    """

    examiner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='exams_author',
        related_query_name='exam_author',
    )
    avaiable = models.BooleanField(default=False)
    created_in = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=500, unique=True)
    topic = models.CharField(max_length=100)
    answered = models.BooleanField(default=False)
    checking = models.BooleanField(default=False)
    judged = models.BooleanField(default=False)
    judged_in = models.DateTimeField(blank=True, null=True)
    archivized = models.BooleanField(default=False)
    archivized_in = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Exam '{self.title}' - by {self.examiner.username} "

    def start_exam(self):
        if not self.avaiable:
            self.avaiable = True

    def stop_exam(self):
        if self.avaiable:
            self.avaiable = False


class Question(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='exam_questions',
        related_query_name='exam_question',
    )
    question_text = models.TextField(max_length=500)
    max_points = models.FloatField(validators=[validate_positive])

    def __str__(self):
        return f'Question {self.id} of exam {self.exam.title}'


class Result(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='results',
        related_query_name='result',
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='result_students',
        related_query_name='result_studnet',
    )
    overall_max_points = models.FloatField(blank=True, null=True)
    scored_points = models.FloatField(blank=True, null=True)
    VERY_GOOD = 5
    GOOD = 4
    NORMAL = 3
    LOW = 2
    FAILED = 1
    GRADE_IN_SCHOOL_CHOICES = (
        (VERY_GOOD, 'Very Good'),
        (GOOD, 'Good'),
        (NORMAL, 'Normal'),
        (LOW, 'Low'),
        (FAILED, 'Failed'),
    )
    grade = models.IntegerField(
        null=True,
        blank=True,
        choices=GRADE_IN_SCHOOL_CHOICES,
    )

    def __str__(self):
        return f'Result user {self.student.username} of exam {self.exam.title}'

    def count_results(self):
        self.overall_max_points = self.exam.exam_questions.aggregate(Sum('max_points')).get('max_points__sum', 0.0)
        self.scored_points = self.exam.exam_assesments.filter(
            student_answer__student=self.student).aggregate(Sum('points')).get('points__sum', 0.0)


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='question_anwsers',
        related_query_name='question_anwser',
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='exam_answers',
        related_query_name='exam_answer',
    )
    student = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='answers_author',
        related_query_name='answer_author',
    )
    answer_text = models.TextField(max_length=1500, blank=True)

    def __str__(self):
        return f'Answer-{self.id} of question-{self.question.id} exam {self.exam.title}'


class Assesment(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='exam_assesments',
        related_query_name='exam_assesment',
    )
    student_answer = models.OneToOneField(
        Answer,
        on_delete=models.CASCADE,
        related_name='answer_assesments',
        related_query_name='answer_assesment',
    )
    result = models.ForeignKey(
        Result,
        on_delete=models.CASCADE,
        related_name='result_assesments',
        related_query_name='result_assesment',
    )
    commentary = models.CharField(max_length=1000, blank=True, null=True)
    points = models.FloatField(validators=[validate_positive], blank=True, null=True)  #Additona limit to max points !!!!!!!

    def __str__(self):
        return f'Assesment- of anwser-{self.student_answer.id} exam {self.exam.title}'
