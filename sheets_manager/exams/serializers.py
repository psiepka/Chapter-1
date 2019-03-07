from rest_framework import serializers
from django.utils import timezone
from exams import models


class ExamSerializer(serializers.HyperlinkedModelSerializer):
    examiner = serializers.ReadOnlyField(source='examiner.username')
    result = serializers.HyperlinkedIdentityField(view_name='exam-result')
    test = serializers.HyperlinkedIdentityField(view_name='exam-test')

    class Meta:
        model = models.Exam
        fields = (
            'url', 'id', 'examiner', 'title', 'topic', 'created_in',
            'avaiable', 'test', 'answered', 'checking', 'judged',
            'result', 'archivized', 'archivized_in'
        )


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = models.Question
        fields = ('id', 'question_text', 'max_points')


class ExamDetailSerializer(serializers.ModelSerializer):
    exam_questions = QuestionSerializer(many=True)
    examiner = serializers.ReadOnlyField(source='examiner.username')
    test = serializers.HyperlinkedIdentityField(view_name='exam-test')
    assesments = serializers.HyperlinkedIdentityField(view_name='exam-assesment')
    set_grades = serializers.HyperlinkedIdentityField(view_name='exam-judge-results')

    class Meta:
        model = models.Exam
        fields = (
            'url', 'id', 'examiner', 'title', 'topic', 'created_in',
            'avaiable', 'test', 'answered', 'assesments', 'checking', 'set_grades',
            'judged', 'archivized', 'archivized_in', 'exam_questions'
        )

    def create(self, validated_data):
        questions_data = validated_data.pop('exam_questions')
        exam = models.Exam.objects.create(**validated_data)
        for question in questions_data:
            models.Question.objects.create(exam=exam, **question_data)
        return exam

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('exam_questions')
        instance.avaiable = validated_data.get('avaiable', instance.avaiable)
        instance.title = validated_data.get('title', instance.title)
        instance.topic = validated_data.get('topic', instance.topic)
        instance.archivized = validated_data.get('archivized', instance.archivized)
        instance.save()
        # Checking questions if some of them are deleted
        questions_preview = [x.id for x in models.Question.objects.filter(exam=instance)]
        questions_actuall = [x.get('id') for x in questions_data if x.get('id') != None]
        for x in questions_preview:
            if x not in questions_actuall:
                models.Question.objects.get(id=x).delete()
        # Adding new and updating questions
        for question in questions_data:
            nr = question.get('id', None)
            if nr:
                q = models.Question.objects.filter(id=nr, exam=instance)
                if q.exists():
                    q = q.first()
                    q.question_text = question.get('question_text', q.question_text)
                    q.max_points = question.get('max_points', q.question_text)
                    q.save()
                else:
                    raise serializers.ValidationError('You cant edit/create question with this id.')
            else:
                models.Question.objects.create(exam=instance, **question)
        return instance


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        user = self.context['request'].user
        data = data.filter(student=user)
        return super(FilteredListSerializer, self).to_representation(data)


class AnswerTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Answer
        list_serializer_class = FilteredListSerializer
        fields = ('answer_text',)


class QuestionTestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    question_anwsers = AnswerTestSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ('id', 'question_text', 'max_points', 'question_anwsers', )
        read_only_fields = ('id', 'question_text', 'max_points',)


class ExamTestSerializer(serializers.ModelSerializer):
    examiner = serializers.ReadOnlyField(source='examiner.username')
    exam_questions = QuestionTestSerializer(many=True, required=False)

    class Meta:
        model = models.Exam
        fields = (
            'examiner', 'title', 'topic','exam_questions'
        )
        read_only_fields = ('title', 'topic')

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if not instance.results.filter(student=user).exists():
            instance.results.create(student=user)
        questions_list = validated_data.get('exam_questions', None)
        if questions_list:
            for que in questions_list:
                q_id = que.get('id', None)
                q = models.Question.objects.filter(exam=instance, id=q_id)
                if q.exists():
                    q = q.first()
                    answer = models.Answer.objects.filter(exam=instance, student=user, question=q)
                    answers = que.get('question_anwsers', None)
                    for ans in answers:
                        if answer.exists():
                            answer = answer.first()
                            answer.answer_text = ans.get('answer_text', answer.answer_text)
                            answer.save()
                        else:
                            models.Answer.objects.create(
                                exam=instance, student=user, question=q, answer_text=ans.get('answer_text','')
                            )
        if not instance.answered:
            instance.answered = True
            instance.save()
        return instance


class AssesmentTestAnswersSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Assesment
        fields = ('commentary', 'points')


class AnswerTestAnswersSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    answer_assesments = AssesmentTestAnswersSerializer()

    class Meta:
        model = models.Answer
        fields = ('id', 'student', 'answer_text', 'answer_assesments')
        read_only_fields = ('id', 'answer_text')


class QuestionTestAnswersSerializer(serializers.ModelSerializer):
    question_anwsers = AnswerTestAnswersSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ('id', 'question_text', 'max_points', 'question_anwsers', )
        read_only_fields = ('id', 'question_text', 'max_points', )


class ExamTestAnswersSerializer(serializers.ModelSerializer):
    examiner = serializers.ReadOnlyField(source='examiner.username')
    exam_questions = QuestionTestAnswersSerializer(many=True, required=False)

    class Meta:
        model = models.Exam
        fields = (
            'url', 'id', 'examiner', 'title', 'topic', 'created_in', 'avaiable', 'answered', 'checking',
            'judged', 'archivized', 'archivized_in', 'exam_questions'
        )

        read_only_fields = (
            'url', 'id', 'examiner', 'title', 'topic', 'created_in', 'avaiable', 'answered', 'checking',
            'judged', 'archivized', 'archivized_in',
        )

    def update(self, instance, validated_data):
        questions_list = validated_data.get('exam_questions', None)
        if questions_list:
            for que in questions_list:
                answers = que.get('question_anwsers', None)
                for ans in answers:
                    answer = models.Answer.objects.filter(id=ans.get('id', None))
                    student = ans.get('student', None)
                    if not instance.results.filter(student=student).exists():
                        instance.results.create(student=student)
                    result = instance.results.filter(student=student).first()
                    rate = ans.get('answer_assesments', None)
                    if answer.exists():
                        answer = answer.first()
                        # Validate points for answer - compare max points of question with point asign for answer
                        max_points = answer.question.max_points
                        if rate.get('points', None) > max_points:
                            raise serializers.ValidationError('Value cant be greater than maximum!')
                        assesment = models.Assesment.objects.filter(
                            exam=instance,
                            student_answer=answer,
                            result=result
                        )
                        if not assesment.exists():
                            instance.exam_assesments.create(
                            student_answer=answer,
                            commentary=rate.get('commentary', None),
                            points=rate.get('points', None),
                            result=result
                        )
                        else:
                            assesment = assesment.first()
                            assesment.commentary=rate.get('commentary', None)
                            assesment.points=rate.get('points', None)
                            assesment.save()
                    else:
                        raise serializers.ValidationError('This answer doesnt exists.')
                    result.count_results()
                    result.save()
        if not instance.checking:
            instance.checking = True
            instance.save()
        return instance


class ResultsOfExamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = models.Result
        fields = (
            "id", "overall_max_points", "scored_points",
            "grade", "exam", "student",
        )
        read_only_fields = (
            "id", "overall_max_points", "scored_points",
            "exam", "student",
        )


class ExamResultsJudgeSerializer(serializers.ModelSerializer):
    results = ResultsOfExamSerializer(many=True)

    class Meta:
        model = models.Exam
        fields = (
            'id', 'title', 'topic', 'created_in',
            'avaiable', 'answered', 'judged', 'archivized', 'results',
        )
        read_only_fields =(
            'id', 'title', 'topic', 'created_in',
            'avaiable', 'answered', 'judged', 'archivized',
        )

    # def validate(self, data):
    #     """Validate value of grade
    #     Arguments:
    #         grade {[int]} -- value of grade input in app
    #     Raises:
    #         serializers.ValidationError -- raise if value not in list of allowed values
    #     """
    #     avaiable_grades = [x[0] for x in models.Result.GRADE_IN_SCHOOL_CHOICES]
    #     grades = data.get('results', None)
    #     for x in grades:
    #         grade = x.get('grade', None)
    #         if grade :
    #             if grade not in avaiable_grades:
    #                 raise serializers.ValidationError(f'This grade doesnt exists! Avaiable grades : {avaiable_grades}')
    #     return data

    def update(self, instance, validated_data):
        results = validated_data.get('results', None)
        for result in results:
            r = instance.results.get(id=result.get('id',None))
            r.grade = result.get('grade', None)
            r.save()
        judge_list = [x.grade for x in instance.results.all()]
        instance.judged = False if None in judge_list else True
        if instance.judged:
            instance.judged_in = timezone.now()
        instance.checking = False if not None in judge_list else True
        instance.save()
        return instance


class AnswerResultSerializer(serializers.ModelSerializer):
    answer_assesments = AssesmentTestAnswersSerializer()

    class Meta:
        model = models.Answer
        list_serializer_class = FilteredListSerializer
        fields = ('answer_text', 'answer_assesments')


class QuestionResultSerializer(serializers.ModelSerializer):
    question_anwsers = AnswerResultSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ('question_text', 'max_points', 'question_anwsers')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        list_serializer_class = FilteredListSerializer
        fields = ('overall_max_points', 'scored_points', 'grade')


class ExamResultDetailSerializer(serializers.ModelSerializer):
    examiner = serializers.ReadOnlyField(source='examiner.username')
    exam_questions = QuestionResultSerializer(many=True)
    results = ResultSerializer(many=True)

    class Meta:
        model = models.Exam
        fields = (
            'id', 'examiner', 'title', 'topic', 'created_in',
            'avaiable', 'answered', 'judged', 'judged_in','archivized',
            'results', 'exam_questions'
        )

class ResultsListSerializer(serializers.ModelSerializer):
    exam = serializers.StringRelatedField(source='exam.title')
    student = serializers.StringRelatedField(source='student.username')
    exam_id = serializers.HyperlinkedRelatedField(queryset=models.Exam, view_name='exam-result')

    class Meta:
        model = models.Result
        fields = (
            'exam', 'student', 'grade', 'exam_id'
        )
