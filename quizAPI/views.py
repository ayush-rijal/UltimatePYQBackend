from rest_framework import generics
from django.http import Http404

from .models import Question,Choice,Category0,Category1, Questions_file
from .serializers import QuestionSerializer,ChoiceSerializer,Category0Serializer,Category1Serializer,Questions_fileSerializer
from rest_framework.pagination import PageNumberPagination


class QuestionPagination(PageNumberPagination):
    page_size=5 # 5 quesitons per page
    page_size_query_param='page_size'
    max_page_size=10


class AllCategory0APIView(generics.ListAPIView):
    queryset=Category0.objects.all()
    serializer_class=Category0Serializer    


class AllCategory1APIView(generics.ListAPIView):
    serializer_class=Category1Serializer  

    def get_queryset(self):
        category0=self.kwargs.get('category0')
        return Category1.objects.filter(category0__name=category0)    


class AllQuestions_fileAPIView(generics.ListAPIView):
    serializer_class=Questions_fileSerializer 

    def get_queryset(self):
        category0=self.kwargs.get('category0')
        category1=self.kwargs.get('category1')
        return Questions_file.objects.filter(category0__name=category0,category1__name=category1)   
    
class AllQuestionAPIView(generics.ListAPIView):
    # queryset=Question.objects.all().order_by('id')
    serializer_class=QuestionSerializer
    pagination_class=QuestionPagination

    def get_queryset(self):
        category0=self.kwargs.get('category0')
        category1=self.kwargs.get('category1')
        questions_file=self.kwargs.get('questions_file')
        return Question.objects.filter(questions_file__category0__name=category0,
         questions_file__category1__name=category1,
         questions_file__title=questions_file
        ).order_by('id')

class AQuestionAPIView(generics.RetrieveAPIView):
    serializer_class=QuestionSerializer
    pagination_class=QuestionPagination

    def get_queryset(self):
        category0=self.kwargs.get('category0')
        category1=self.kwargs.get('category1')
        questions_file=self.kwargs.get('questions_file')
        question_id=self.kwargs.get('pk')

        return Question.objects.filter(questions_file__category0__name=category0,
         questions_file__category1__name=category1,
         questions_file__title=questions_file,
         id=question_id
        )                             
        

class AllChoiceOfAQuestionAPIView(generics.ListAPIView):
    serializer_class=ChoiceSerializer

    def get_queryset(self):
        category0=self.kwargs.get('category0')
        category1=self.kwargs.get('category1')
        questions_file=self.kwargs.get('questions_file')
        question_id=self.kwargs.get('pk')

        return Choice.objects.filter(question__questions_file__category0__name=category0,
         question__questions_file__category1__name=category1,
         question__questions_file__title=questions_file,
         question__id=question_id
        )