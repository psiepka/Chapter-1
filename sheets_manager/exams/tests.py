"""
Tests of features exams
"""

from rest_framework.test import APITestCase, force_authenticate
from rest_framework import  status
from rest_framework.reverse import reverse
from .models import User, Exam, Answer, Assesment, Result, Question


class ExamTestCase(APITestCase):
    """
    Testing all models, urls methods, permissions in exams app.

    """


    @classmethod
    def setUpClass(cls):
        """
        Once for all tests
        """

        cls.u1 = User.objects.create_user(
            username="User_1", first_name='Name_1', last_name='Surname_1', password='pass'
        )
        cls.u2 = User.objects.create_user(
            username="User_2", first_name='Name_2', last_name='Surname_2', password='pass'
        )
        cls.u3 = User.objects.create_user(
            username="User_3", first_name='Name_3', last_name='Surname_3', password='pass'
        )
        cls.u4 = User.objects.create_user(
            username="User_4", first_name='Name_4', last_name='Surname_4', password='pass'
        )
        cls.exam = Exam.objects.create(examiner=cls.u1, title='First exam test', topic='TESTS')
        cls.exam2 = Exam.objects.create(examiner=cls.u1, title='Secound exam test', topic='TESTS')
        cls.q1 = Question.objects.create(exam=cls.exam, question_text='Question nr 1', max_points=5)
        cls.q2 = Question.objects.create(exam=cls.exam, question_text='Question nr 2', max_points=5)
        cls.q3 = Question.objects.create(exam=cls.exam, question_text='Question nr 3', max_points=5)
        cls.ans11 = Answer.objects.create(exam=cls.exam, question=cls.q1, student=cls.u2, answer_text='ans1-u2')
        cls.ans21 = Answer.objects.create(exam=cls.exam, question=cls.q2, student=cls.u2, answer_text='ans2-u2')
        cls.ans31 = Answer.objects.create(exam=cls.exam, question=cls.q3, student=cls.u2, answer_text='ans3-u2')
        cls.ans12 = Answer.objects.create(exam=cls.exam, question=cls.q1, student=cls.u3, answer_text='ans1-u3')
        cls.ans22 = Answer.objects.create(exam=cls.exam, question=cls.q2, student=cls.u3, answer_text='ans2-u3')
        cls.ans32 = Answer.objects.create(exam=cls.exam, question=cls.q3, student=cls.u3, answer_text='ans3-u3')
        cls.ans13 = Answer.objects.create(exam=cls.exam, question=cls.q1, student=cls.u4, answer_text='ans1-u4')
        cls.ans23 = Answer.objects.create(exam=cls.exam, question=cls.q2, student=cls.u4, answer_text='ans2-u4')
        cls.ans33 = Answer.objects.create(exam=cls.exam, question=cls.q3, student=cls.u4, answer_text='ans3-u4')
        cls.res1 = Result.objects.create(exam=cls.exam, student=cls.u2)
        cls.res2 = Result.objects.create(exam=cls.exam, student=cls.u3)
        cls.ev11 = Assesment.objects.create(exam=cls.exam, student_answer=cls.ans11, result=cls.res1, commentary='mogłobyc lepeij', points=1)
        cls.ev21 = Assesment.objects.create(exam=cls.exam, student_answer=cls.ans21, result=cls.res1, commentary='mogłobyc lepeij', points=1)
        cls.ev31 = Assesment.objects.create(exam=cls.exam, student_answer=cls.ans31, result=cls.res1, commentary='mogłobyc lepeij', points=1)
        cls.ev12 = Assesment.objects.create(exam=cls.exam, student_answer=cls.ans12, result=cls.res2, commentary='mogłobyc lepeij', points=5)
        cls.ev22 = Assesment.objects.create(exam=cls.exam, student_answer=cls.ans22, result=cls.res2, commentary='mogłobyc lepeij', points=5)
        r1 = cls.res1
        r2 = cls.res2
        r1.count_results()
        r2.count_results()
        r1.save()
        r2.save()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_exam_users(self):
        """
        Simple verify the proper setting up tests
        """

        self.assertEqual(self.u1, self.exam.examiner)
        self.assertFalse(self.exam.examiner == self.u2)
        self.assertTrue(self.ans11.student == self.u2)
        self.assertFalse(self.ans11.student == self.u1)
        self.assertTrue(self.ans11.exam.examiner == self.u1)
        self.assertEqual(Exam.objects.filter(examiner=self.u2).count(), 0)

    def test_exam_questions(self):
        """
        Simple verify the proper setting up tests
        """

        self.assertEqual(self.exam.exam_questions.count(), 3)
        self.assertEqual(self.exam2.exam_questions.count(), 0)

    def test_exam_answers(self):
        """
        Simple verify the proper setting up tests
        """
        self.assertEqual(self.exam.exam_answers.filter(student=self.u2).count(), 3)
        self.assertEqual(self.exam.exam_answers.filter(student=self.u3).count(), 3)
        self.assertEqual(self.exam.exam_answers.filter(student=self.u4).count(), 3)

    def test_exam_assesment(self):
        """
        Simple verify the proper setting up tests
        """
        eval1 = Assesment.objects.get(student_answer=self.ans11, student_answer__student=self.u2)
        eval1_len = Assesment.objects.filter(student_answer=self.ans11, student_answer__student=self.u2)
        self.assertEqual(eval1.points, 1)
        self.assertEqual(eval1_len.count(), 1)
        eval2 = Assesment.objects.get(student_answer=self.ans12, student_answer__student=self.u3)
        eval2_len = Assesment.objects.filter(student_answer=self.ans12, student_answer__student=self.u3)
        self.assertEqual(eval1.points, 1)
        self.assertEqual(eval1_len.count(), 1)

    def test_get_exam_list(self):
        """
        Simple verify the proper functioning of main page exams
        """
        data = {}
        url = reverse('exam-list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_anonymuos_exam_forbidden(self):
        """
        Simple verify methods allowed on main page to anonymous users
        """
        data = {
            'title':'bleblebleb',
            'topic':'aFftłefłe'
        }
        url = reverse('exam-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_exam_create_user(self):
        """
        Simple verify methods allowed on main page to register users and correct creating a model of Exam
        """
        data = {
            'title':'bleblebleb',
            'topic':'aFftłefłe'
        }
        login = self.client.login(username='User_2', password='pass')
        url = reverse('exam-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_exam = Exam.objects.get(
            title=data['title'],
            topic=data['topic'],
        )
        url = reverse('exam-detail', args=[new_exam.id])
        response = self.client.get(url, data, format='json')
        self.assertFalse(new_exam.avaiable)
        self.assertFalse(new_exam.answered)
        self.assertFalse(new_exam.checking)
        self.assertFalse(new_exam.judged)
        self.assertFalse(new_exam.archivized)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_exam_bad_create(self):
        """
        Simple verify incorrect creating a model of Exam
        """
        data = {
        }
        login = self.client.login(username='User_2', password='pass')
        url = reverse('exam-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detail_exam(self):
        """
        Simple verify access allowed on viewing detail of exam to anonymous users
        """
        data = {}
        url = reverse('exam-detail', args=[1])
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_exam_by_examiner(self):
        """
        Simple verify access allowed on viewing detail of exam to author of Exam
        """
        data = {}
        url = reverse('exam-detail', args=[1])
        login = self.client.login(username='User_1', password='pass')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_exam_by_student(self):
        """
        Simple verify access allowed on viewing detail of exam to register users wha are not author of exam
        """
        data = {}
        url = reverse('exam-detail', args=[1])
        login = self.client.login(username='User_2',password='pass')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_exam_update_by_examiner(self):
        """
        Simple verify corrrect updates of Exam details by author
        """
        data = {
            "id": 1,
            "title": "First exam test",
            "topic": "TESTS",
            "exam_questions": [
                {
                    "question_text": "Which is more effective accordding to bearing -steel or concrete brigde? Why?",
                    "max_points": 0.7
                }
            ]
        }
        exam = Exam.objects.get(id=1)
        url = reverse('exam-detail', args=[exam.id])
        login = self.client.login(username='User_1',password='pass')
        self.assertEqual(exam.exam_questions.all().count(), 3)
        response = self.client.put(url, data, format='json')
        self.assertEqual(exam.exam_questions.all().count(), 1)
        self.assertEqual(exam.exam_questions.first().question_text, data['exam_questions'][0]['question_text'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_exam_update_by_student(self):
        """
        Verify corrrect adding Question to Exam by author
        """
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

    def test_exam_archives_correct(self):
        """
        Verify correct archives exams by owner
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-detail', args=[exam.id])
        login = self.client.login(username='User_1',password='pass')
        self.assertEqual(exam.archivized, False)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Exam.objects.get(id=1).archivized, True)

    def test_exam_archves_delete_correct(self):
        """
        Verify correct delete archives exams by owner
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-detail', args=[exam.id])
        login = self.client.login(username='User_1',password='pass')
        self.assertEqual(exam.archivized, False)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Exam.objects.get(id=1).archivized, True)
        self.assertEqual(exam.archivized, False)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        new_response = self.client.get(url)
        self.assertEqual(new_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_exam_archves_incorrect(self):
        """
        Verify archives exams by not owner
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-detail', args=[exam.id])
        login = self.client.login(username='User_2',password='pass')
        self.assertEqual(exam.archivized, False)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Exam.objects.get(id=1).archivized, False)

    def test_exam_test_forbidden(self):
        """
        Verify access to exam test without permission
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-test', args=[exam.id])
        login = self.client.login(username='User_2',password='pass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exam_test_avaiable(self):
        """
        Verify access to exam test with permission
        """
        exam = Exam.objects.get(id=1)
        exam.avaiable = True
        exam.save()
        url = reverse('exam-test', args=[exam.id])
        login = self.client.login(username='User_2',password='pass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exam_test_avaiable_good_add_new(self):
        """
        Verify adding answers by students
        """
        u5 = User.objects.create_user(
            username="User_5", first_name='Name_5', last_name='Surname_4', password='pass'
        )
        u5.save()
        exam = Exam.objects.get(id=1)
        exam.avaiable = True
        exam.save()
        url = reverse('exam-test', args=[exam.id])
        login = self.client.login(username='User_5',password='pass')
        data = {
            "exam_questions":[
                {
                    "id": 1,
                    "question_anwsers": [
                        {
                            "answer_text": "odp number one"
                        }
                    ]
                },
                {
                    "id": 2,
                    "question_anwsers": [
                        {
                            "answer_text": "odp number two",

                        }
                    ]
                },
                {
                    "id": 3,
                    "question_text": "Pytanie zamienione !",
                    "max_points": 1,
                    "question_anwsers": [
                        {
                            "answer_text": "odp number three",
                        }
                    ]
                }
            ]
        }
        self.assertEqual(
            User.objects.get(username='User_5').answers_author.all().count(),
            0
        )
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            User.objects.get(username='User_5').answers_author.all().count(),
            3
        )
        self.assertEqual(Question.objects.get(id=3).question_text, 'Question nr 3')

    def test_exam_test_avaiable_good_update(self):
        """
        Verify update answers by students
        """
        exam = Exam.objects.get(id=1)
        exam.avaiable = True
        exam.save()
        url = reverse('exam-test', args=[exam.id])
        login = self.client.login(username='User_2',password='pass')
        self.assertEqual(
            User.objects.get(username='User_2').answers_author.all().count(),
            3
        )
        self.assertEqual(
            Question.objects.get(id=1).question_anwsers.get(
                student=User.objects.get(username='User_2')
            ).answer_text,
            'ans1-u2'
        )
        data = {
            "exam_questions":[
                {
                    "id": 1,
                    "question_anwsers": [
                        {
                            "answer_text": "odp number one"
                        }
                    ]
                },
                {
                    "id": 3,
                    "question_anwsers": [
                        {
                            "answer_text": "odp number three",
                        }
                    ]
                }
            ]
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(
            User.objects.get(username='User_2').answers_author.all().count(),
            3
        )
        self.assertEqual(
            Question.objects.get(id=1).question_anwsers.get(
                student=User.objects.get(username='User_2')
            ).answer_text,
            'odp number one'
        )
        self.assertEqual(
            Question.objects.get(id=2).question_anwsers.get(
                student=User.objects.get(username='User_2')
            ).answer_text,
            'ans2-u2'
        )
        self.assertEqual(
            Question.objects.get(id=3).question_anwsers.get(
                student=User.objects.get(username='User_2')
            ).answer_text,
            'odp number three'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exam_test_avaiable_update_question_by_student(self):
        """
        Verify making changes to question in test by students
        """
        exam = Exam.objects.get(id=1)
        exam.avaiable = True
        exam.save()
        url = reverse('exam-test', args=[exam.id])
        login = self.client.login(username='User_2',password='pass')
        data = {
            "exam_questions":[
                {
                    "id": 3,
                    "question_text": "Pytanie zamienione !",
                    "max_points": 1,
                    "question_anwsers": [
                        {
                            "answer_text": "Odpowiedz 3",
                        }
                    ]
                }
            ]
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(
            User.objects.get(username='User_2').answers_author.all().count(),
            3
        )
        self.assertEqual(
            Question.objects.get(id=3).question_anwsers.get(
                student=User.objects.get(username='User_2')
            ).answer_text,
            'Odpowiedz 3'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Question.objects.get(id=3).question_text != 'Pytanie zamienione !')
        self.assertEqual(Question.objects.get(id=3).question_text, 'Question nr 3')
        self.assertTrue(Question.objects.get(id=3).max_points != 1)

    def test_exam_result_and_assesment_new_added(self):
        """
        Verify create assesment by examiner
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-assesment', args=[exam.id])
        login = self.client.login(username='User_1',password='pass')
        u = User.objects.get(id=4)
        self.assertFalse(Exam.objects.get(id=1).checking)
        self.assertEqual(
            exam.results.filter(student=u).count(),
            0
        )
        data = {
            "id": 1,
            "exam_questions": [
                {
                    "id": 1,
                    "question_anwsers": [
                        {
                            "id": 7,
                            "student": 4,
                            "answer_assesments": {
                                "commentary": "Nice one",
                                "points": 0.0
                            }
                        },
                    ]
                },
                {
                    "id": 2,
                    "question_anwsers": [
                        {
                            "id": 8,
                            "student": 4,
                            "answer_assesments": {
                                "commentary": "Nice one",
                                "points": 1.0
                            }
                        },
                    ]
                },
            ]
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(
            exam.results.filter(student=u).count(),
            1
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Exam.objects.get(id=1).checking)
        self.assertEqual(User.objects.get(id=4).result_students.get(exam=exam, student=u).scored_points, 1)
        self.assertEqual(User.objects.get(id=4).result_students.get(exam=exam, student=u).overall_max_points, 15)

    def test_exam_assesment_new_forbidden(self):
        """
        Verify access to assesment exams by students
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-assesment', args=[exam.id])
        login = self.client.login(username='User_2',password='pass')
        data = {
            "id": 1,
            "exam_questions": [
                {
                    "id": 1,
                    "question_anwsers": [
                        {
                            "id": 7,
                            "student": 4,
                            "answer_assesments": {
                                "commentary": "Nice one",
                                "points": 0.0
                            }
                        },
                    ]
                },
                {
                    "id": 2,
                    "question_anwsers": [
                        {
                            "id": 8,
                            "student": 4,
                            "answer_assesments": {
                                "commentary": "Nice one",
                                "points": 1.0
                            }
                        },
                    ]
                },
            ]
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exam_result_and_assesment_update(self):
        """
        Verify updates to assesment exams by examiner
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-assesment', args=[exam.id])
        login = self.client.login(username='User_1',password='pass')
        u = User.objects.get(id=2)
        self.assertEqual(
            exam.results.filter(student=u).count(),
            1
        )
        self.assertEqual(User.objects.get(id=2).result_students.get(exam=exam, student=u).scored_points, 3)
        self.assertEqual(User.objects.get(id=2).result_students.get(exam=exam, student=u).overall_max_points, 15)
        data = {
            "id": 1,
            "exam_questions": [
                {
                    "id": 1,
                    "question_anwsers": [
                        {
                            "id": 1,
                            "student": 2,
                            "answer_assesments": {
                                "commentary": "Updated-1",
                                "points": 0.0
                            }
                        },
                    ]
                },
                {
                    "id": 2,
                    "question_anwsers": [
                        {
                            "id": 2,
                            "student": 2,
                            "answer_assesments": {
                                "commentary": "Updated-2",
                                "points": 5.0
                            }
                        },
                    ]
                },
            ]
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(
            exam.results.filter(student=u).count(),
            1
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Exam.objects.get(id=1).checking)
        self.assertEqual(Assesment.objects.get(exam=exam, student_answer=1).commentary, 'Updated-1')
        self.assertEqual(User.objects.get(id=2).result_students.get(exam=exam, student=u).scored_points, 6)
        self.assertEqual(User.objects.get(id=2).result_students.get(exam=exam, student=u).overall_max_points, 15)

    def test_exam_result_and_assesment_update_over_points(self):
        """
        Verify bad requestes - over max points to assesment exams by students
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-assesment', args=[exam.id])
        login = self.client.login(username='User_1',password='pass')
        data = {
            "id": 1,
            "exam_questions": [
                {
                    "id": 1,
                    "question_anwsers": [
                        {
                            "id": 1,
                            "student": 2,
                            "answer_assesments": {
                                "commentary": "Updated-1",
                                "points": 0.0
                            }
                        },
                    ]
                },
                {
                    "id": 2,
                    "question_anwsers": [
                        {
                            "id": 2,
                            "student": 2,
                            "answer_assesments": {
                                "commentary": "Points > max points",
                                "points": 6.0
                            }
                        },
                    ]
                },
            ]
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exam_result_and_assesment_update_under_points(self):
        """
        Verify bad requestes - negative points to assesment exams by students
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-assesment', args=[exam.id])
        login = self.client.login(username='User_1', password='pass')
        data = {
            "id": 1,
            "exam_questions": [
                {
                    "id": 1,
                    "question_anwsers": [
                        {
                            "id": 1,
                            "student": 2,
                            "answer_assesments": {
                                "commentary": "Updated-1",
                                "points": 0.0
                            }
                        },
                    ]
                },
                {
                    "id": 2,
                    "question_anwsers": [
                        {
                            "id": 2,
                            "student": 2,
                            "answer_assesments": {
                                "commentary": "Negative points not allowed",
                                "points": -6.0
                            }
                        },
                    ]
                },
            ]
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exam_results_judge_forbidden(self):
        """
        Verify bad requestes - incorrect grade in result model of exams by students
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-judge-results', args=[exam.id])
        response_anon = self.client.get(url)
        self.assertEqual(response_anon.status_code, status.HTTP_403_FORBIDDEN)
        login = self.client.login(username='User_2',password='pass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exam_results_judge_bad_grade(self):
        exam = Exam.objects.get(id=1)
        url = reverse('exam-judge-results', args=[exam.id])
        login = self.client.login(username='User_1',password='pass')
        data = {
            "id": 1,
            "results": [
                {
                    "id": 1,
                    "exam": 1,
                    "student": 2,
                    "grade": 7
                },
            ]
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exam_results_all_judged(self):
        """
        Verify exam atributes after judge every tests in exam
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-judge-results', args=[exam.id])
        login = self.client.login(username='User_1',password='pass')
        data = {
            "id": 1,
            "results": [
                {
                    "id": 1,
                    "exam": 1,
                    "student": 2,
                    "grade": 5
                },
                {
                    "id": 2,
                    "exam": 1,
                    "student": 3,
                    "grade": 1
                }
            ]
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Exam.objects.get(id=1).judged)
        self.assertFalse(Exam.objects.get(id=1).checking)

    def test_exam_results_half_judged(self):
        """
        Verify exam atributes after judge not every tests in exam
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-judge-results', args=[exam.id])
        login = self.client.login(username='User_1',password='pass')
        data = {
            "id": 1,
            "results": [
                {
                    "id": 1,
                    "exam": 1,
                    "student": 2,
                    "grade": 5
                },
            ]
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Exam.objects.get(id=1).checking)
        self.assertFalse(Exam.objects.get(id=1).judged)

    def test_exam_result_view_anon_before(self):
        """
        Verify access to result page of exam by anonymous user before examiner permission
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-result', args=[exam.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exam_result_view_anon_after(self):
        """
        Verify access to result page of exam by anonymous user before examiner permission
        """
        exam = Exam.objects.get(id=1)
        exam.judged = True
        exam.save()
        exam = Exam.objects.get(id=1)
        url = reverse('exam-result', args=[exam.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exam_result_view_user_before_judge(self):
        """
        Verify access to result page of exam by register user before examiner permission
        """
        exam = Exam.objects.get(id=1)
        url = reverse('exam-result', args=[exam.id])
        login = self.client.login(username='User_2',password='pass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exam_result_view_not_student(self):
        """
        Verify access to result page of exam by new register user
        (not student, not person who particiapte in test) after examiner permission
        """
        u5 = User.objects.create_user(
            username="User_5", first_name='Name_5', last_name='Surname_5', password='pass'
        )
        u5.save()
        exam = Exam.objects.get(id=1)
        exam.judged = True
        exam.save()
        url = reverse('exam-result', args=[exam.id])
        login = self.client.login(username='User_5',password='pass')
        response = self.client.get(url)
        self.assertFalse(response.data['results'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exam_result_view_student(self):
        """
        Verify view of result page exam by student
        """
        exam = Exam.objects.get(id=1)
        exam.judged = True
        exam.save()
        url = reverse('exam-result', args=[exam.id])
        login = self.client.login(username='User_2', password='pass')
        response = self.client.get(url)
        self.assertTrue(response.data['results'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exam_result_edit_student(self):
        """
        Verify using another method than get on result page
        """
        exam = Exam.objects.get(id=1)
        exam.judged = True
        exam.save()
        url = reverse('exam-result', args=[exam.id])
        login = self.client.login(username='User_2', password='pass')
        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
