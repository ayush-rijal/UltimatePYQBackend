from rest_framework import generics
from django.http import Http404
from .models import Question,Choice,Category0,Category1, Questions_file,UserQuizResult,UserResponse,Leaderboard
from .serializers import QuestionSerializer,ChoiceSerializer,Category0Serializer,Category1Serializer,Questions_fileSerializer,UserQuizResultSerializer,UserResponseSerializer,LeaderboardSerializer

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum

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

class SubmitQuizAPIView(APIView):
    def post(self, request, category0, category1, questions_file):
        # Expecting {"choices": {question_id: choice_id, ...}, "is_submitted": true}
        choices = request.data.get("choices", {})
        is_submitted = request.data.get("is_submitted", True)

        if not choices:
            return Response({"error": "No choices provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Questions_file
        questions_file_obj = get_object_or_404(
            Questions_file,
            category0__name=category0,
            category1__name=category1,
            title=questions_file
        )

        # Process each answer
        responses = []
        for question_id, choice_id in choices.items():
            question = get_object_or_404(Question, id=question_id, questions_file=questions_file_obj)
            choice = get_object_or_404(Choice, id=choice_id, question=question)
            response_data = {
                "question": question.id,
                "selected_choice": choice.id,
                "is_submitted": is_submitted
            }
            # Upsert: Update if exists, create if not
            try:
                response=UserResponse.objects.get(user=request.user, question=question)
                serializer = UserResponseSerializer(response,data=response_data,context={'request':request})


            except UserResponse.DoesNotExist:
                serializer=UserResponseSerializer(data=response_data,context={'request':request})    

            if serializer.is_valid():
                serializer.save(user=request.user)
                responses.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Ensure UserQuizResult is updated
        result, _ = UserQuizResult.objects.get_or_create(
            user=request.user,
            questions_file=questions_file_obj
        )
        result.update_points()  # Updates points based on submitted responses

        return Response({
            "status": "quiz submitted",
            "points": result.points,
            "total_questions": Question.objects.filter(questions_file=questions_file_obj).count(),
            "responses":responses
            
        }, status=status.HTTP_201_CREATED)

class QuizResultAPIView(generics.RetrieveAPIView):
    serializer_class = UserQuizResultSerializer

    def get_object(self):
        return get_object_or_404(
            UserQuizResult,
            user=self.request.user,
            questions_file__category0__name=self.kwargs.get('category0'),
            questions_file__category1__name=self.kwargs.get('category1'),
            questions_file__title=self.kwargs.get('questions_file')
        )


# class GlobalLeaderboardAPIView(generics.ListAPIView):
#     serializer_class = LeaderboardSerializer
    
#     def get_queryset(self):
#         return Leaderboard.objects.all().order_by('-total_points')


import logging

logger = logging.getLogger(__name__)

class GlobalLeaderboardAPIView(APIView):
    def get(self, request):
        print("Leaderboard endpoint hit!")  # Add this
        # Fetch raw queryset
        queryset = Leaderboard.objects.all().order_by('-total_points')
        logger.info(f"Raw queryset: {list(queryset)}")  # Log raw data
        if not queryset.exists():
            logger.info("No leaderboard entries found.")
            return Response({"message": "No leaderboard entries available"}, status=200)

        # Serialize
        serializer = LeaderboardSerializer(queryset, many=True)
        logger.info(f"Serialized data: {serializer.data}")  # Log serialized output
        return Response(serializer.data)


   