from django.test import TestCase
from .models import User, Exam, Answer, Assesment, Result, Question


class ExamTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username="User_1", first_name='Name_1', last_name='Surname_1')
        self.u2 = User.objects.create_user(username="User_2", first_name='Name_2', last_name='Surname_2')
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
        self.ev11 = Assesment.objects.create(exam=self.exam, question=self.q1, student_answer=self.ans11, commentary='mogłobyc lepeij',points=1)
        self.ev21 = Assesment.objects.create(exam=self.exam, question=self.q2, student_answer=self.ans21, commentary='mogłobyc lepeij',points=1)
        self.ev31 = Assesment.objects.create(exam=self.exam, question=self.q3, student_answer=self.ans31, commentary='mogłobyc lepeij',points=1)
        self.ev12 = Assesment.objects.create(exam=self.exam, question=self.q1, student_answer=self.ans12, commentary='mogłobyc lepeij',points=5)
        self.ev22 = Assesment.objects.create(exam=self.exam, question=self.q2, student_answer=self.ans22, commentary='mogłobyc lepeij',points=5)
        self.res1 = Result.objects.create(exam=self.exam, student=self.u2)
        self.res2 = Result.objects.create(exam=self.exam, student=self.u3)
        self.res3 = Result.objects.create(exam=self.exam, student=self.u4)

    def test_exam_users(self):
        self.assertEqual(self.u1, self.exam.examiner)
        self.assertFalse(self.exam.examiner == self.u2)
        self.assertTrue(self.ans11.student == self.u2)
        self.assertFalse(self.ans11.student == self.u1)
        self.assertTrue(self.ans11.exam.examiner == self.u1)

    def test_exam_questions(self):
        self.assertEqual(self.exam.exam_questions.count(), 3)
        self.assertEqual(self.exam2.exam_questions.count(), 0)

    def test_exam_answers(self):
        self.assertEqual(self.exam.exam_answers.filter(student=self.u2).count(), 3)
        self.assertEqual(self.exam.exam_answers.filter(student=self.u3).count(), 3)
        self.assertEqual(self.exam.exam_answers.filter(student=self.u4).count(), 1)

    def test_exam_assesment(self):
        eval1 = Assesment.objects.get(question=self.q1, student_answer__student=self.u2)
        eval1_len = Assesment.objects.filter(question=self.q1, student_answer__student=self.u2)
        self.assertEqual(eval1.points, 1)
        self.assertEqual(eval1_len.count(), 1)
        eval2 = Assesment.objects.get(question=self.q1, student_answer__student=self.u3)
        eval2_len = Assesment.objects.filter(question=self.q1, student_answer__student=self.u3)
        self.assertEqual(eval1.points, 1)
        self.assertEqual(eval1_len.count(), 1)
