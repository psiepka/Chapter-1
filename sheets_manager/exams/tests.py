"""
Tests of features exams
"""

from rest_framework.test import APITestCase
from rest_framework import  status
from rest_framework.reverse import reverse
from .models import User, Exam, Answer, Assesment, Result, Question


class ExamTestCase(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username="User_1", first_name='Name_1', last_name='Surname_1', password='pass')
        self.u2 = User.objects.create_user(username="User_2", first_name='Name_2', last_name='Surname_2', password='pass')
        self.u3 = User.objects.create_user(username="User_3", first_name='Name_3', last_name='Surname_3')
        self.u4 = User.objects.create_user(username="User_4", first_name='Name_4', last_name='Surname_4')
        self.exam = Exam.objects.create(examiner=self.u1, title='First exam test', topic='TESTS')
        self.exam2 = Exam.objects.create(examiner=self.u1, title='Secound exam test', topic='TESTS')
        self.q1 = Question.objects.create(exam=self.exam, question_text='Question nr 1', max_points=5)
        self.q2 = Question.objects.create(exam=self.exam, question_text='Question nr 2', max_points=5)
        self.q3 = Question.objects.create(exam=self.exam, question_text='Question nr 3', max_points=5)
        self.ans11 = Answer.objects.create(exam=self.exam, question=self.q1, student=self.u2, answer_text='ans1-u2')
        self.ans21 = Answer.objects.create(exam=self.exam, question=self.q2, student=self.u2, answer_text='ans2-u2')
        self.ans31 = Answer.objects.create(exam=self.exam, question=self.q3, student=self.u2, answer_text='ans3-u2')
        self.ans12 = Answer.objects.create(exam=self.exam, question=self.q1, student=self.u3, answer_text='ans1-u3')
        self.ans22 = Answer.objects.create(exam=self.exam, question=self.q2, student=self.u3, answer_text='ans2-u3')
        self.ans32 = Answer.objects.create(exam=self.exam, question=self.q3, student=self.u3, answer_text='ans3-u3')
        self.ans13 = Answer.objects.create(exam=self.exam, question=self.q1, student=self.u4, answer_text='ans1-u4')
        self.res1 = Result.objects.create(exam=self.exam, student=self.u2)
        self.res2 = Result.objects.create(exam=self.exam, student=self.u3)
        self.res3 = Result.objects.create(exam=self.exam, student=self.u4)
        self.ev11 = Assesment.objects.create(exam=self.exam, student_answer=self.ans11, result=self.res1, commentary='mogłobyc lepeij', points=1)
        self.ev21 = Assesment.objects.create(exam=self.exam, student_answer=self.ans21, result=self.res1, commentary='mogłobyc lepeij', points=1)
        self.ev31 = Assesment.objects.create(exam=self.exam, student_answer=self.ans31, result=self.res1, commentary='mogłobyc lepeij', points=1)
        self.ev12 = Assesment.objects.create(exam=self.exam, student_answer=self.ans12, result=self.res2, commentary='mogłobyc lepeij', points=5)
        self.ev22 = Assesment.objects.create(exam=self.exam, student_answer=self.ans22, result=self.res2, commentary='mogłobyc lepeij', points=5)

    def test_exam_users(self):
        self.assertEqual(self.u1, self.exam.examiner)
        self.assertFalse(self.exam.examiner == self.u2)
        self.assertTrue(self.ans11.student == self.u2)
        self.assertFalse(self.ans11.student == self.u1)
        self.assertTrue(self.ans11.exam.examiner == self.u1)
        self.assertEqual(Exam.objects.filter(examiner=self.u2).count(), 0)

    def test_exam_questions(self):
        self.assertEqual(self.exam.exam_questions.count(), 3)
        self.assertEqual(self.exam2.exam_questions.count(), 0)

    def test_exam_answers(self):
        self.assertEqual(self.exam.exam_answers.filter(student=self.u2).count(), 3)
        self.assertEqual(self.exam.exam_answers.filter(student=self.u3).count(), 3)
        self.assertEqual(self.exam.exam_answers.filter(student=self.u4).count(), 1)

    def test_exam_assesment(self):
        eval1 = Assesment.objects.get(student_answer=self.ans11, student_answer__student=self.u2)
        eval1_len = Assesment.objects.filter(student_answer=self.ans11, student_answer__student=self.u2)
        self.assertEqual(eval1.points, 1)
        self.assertEqual(eval1_len.count(), 1)
        eval2 = Assesment.objects.get(student_answer=self.ans12, student_answer__student=self.u3)
        eval2_len = Assesment.objects.filter(student_answer=self.ans12, student_answer__student=self.u3)
        self.assertEqual(eval1.points, 1)
        self.assertEqual(eval1_len.count(), 1)

    def test_get_exam_list(self):
        data = {}
        url = reverse('exam-list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_exam(self):
        data = {
            'title':'bleblebleb',
            'topic':'aFftłefłe'
        }
        login = self.client.login(username='User_2',password='pass_FAIL')
        url = reverse('exam-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_exam_jwt(self):
        data = {
            'title':'bleblebleb',
            'topic':'aFftłefłe'
        }
        login = self.client.login(username='User_2',password='pass')
        url = reverse('exam-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_exam(self):
        data = {}
        url = reverse('exam-detail', args=[1])
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_exam_by_examiner(self):
        data = {}
        url = reverse('exam-detail', args=[1])
        login = self.client.login(username='User_1',password='pass')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_exam_by_student(self):
        data = {}
        url = reverse('exam-detail', args=[1])
        login = self.client.login(username='User_2',password='pass')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_exam_update_by_examiner(self):
        data = {
            "title": "Last exam number 3",
            "topic": "Building",
            "exam_questions": [
                {
                    "question_text": "Which is more effective accordding to bearing -steel or concrete brigde? Why?",
                    "max_points": 0.7
                }
            ]
        }
        url = reverse('exam-detail', args=[1])
        login = self.client.login(username='User_1',password='pass')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_exam_update_by_student(self):
        data = {
            "title": "Last exam number 3",
            "topic": "Building",
            "exam_questions": [
                {
                    "question_text": "Which is more effective accordding to bearing -steel or concrete brigde? Why?",
                    "max_points": 0.7
                }
            ]
        }
        url = reverse('exam-detail', args=[1])
        login = self.client.login(username='User_2',password='pass')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)