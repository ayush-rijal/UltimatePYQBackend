from rest_framework import generics
from django.http import Http404
from .models import Question,Choice,Category,Questions_file,UserQuizResult,UserResponse,Leaderboard
from .serializers import QuestionSerializer,ChoiceSerializer,CategorySerializer,Questions_fileSerializer,UserQuizResultSerializer,UserResponseSerializer,LeaderboardSerializer

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


class AllCategoriesAPIView(generics.ListAPIView):
    queryset=Category.objects.filter(parent__isnull=True) #Root categories only
    serializer_class=CategorySerializer

class CategoryChildrenAPIView(generics.ListAPIView):
    serializer_class=CategorySerializer

    def get_queryset(self):
        category_path=self.kwargs.get('category_path','').split('/')
        if not category_path or category_path==['']:
            return Category.objects.filter(parent__isnull=True)
        try:
            current_category=Category.objects.get(name=category_path[-1])
            return Category.objects.filter(parent=current_category)
        except Category.DoesNotExist:
            raise Http404("Category not found")    


class AllQuestions_fileAPIView(generics.ListAPIView):
    serializer_class=Questions_fileSerializer 
    

    def get_queryset(self):
        category_path=self.kwargs.get('category_path','').split('/')
        if not category_path or category_path==['']:
            return Questions_file.objects.all()
        try:
            last_category=Category.objects.get(name=category_path[-1])
            print(f"Last category: {last_category}")
            queryset=Questions_file.objects.filter(category=last_category)
            print(f"Files found: {list(queryset)}")
            return queryset
        except Category.DoesNotExist:
            return Questions_file.objects.none()  # Return an empty queryset if the category doesn't exist

   
    
class AllQuestionAPIView(generics.ListAPIView):
    # queryset=Question.objects.all().order_by('id')
    serializer_class=QuestionSerializer
    pagination_class=QuestionPagination

    def get_queryset(self):
        category_path=self.kwargs.get('category_path','').split('/')
        questions_file_title=self.kwargs.get('questions_file', '')
        if not category_path or not questions_file_title:
            return Question.objects.none()
        
        try:
            last_category=Category.objects.get(name=category_path[-1])
            questions_file=Questions_file.objects.get(title=questions_file_title,category=last_category)
            return Question.objects.filter(questions_file=questions_file).order_by('id')
        except (Category.DoesNotExist,Questions_file.DoesNotExist):
            return Question.objects.none()

class AQuestionAPIView(generics.RetrieveAPIView):
    serializer_class=QuestionSerializer
    lookup_field='pk'

    def get_queryset(self):
        category_path=self.kwargs.get('category_path','').split('/')
        questions_file_title=self.kwargs.get('questions_file','')

        try:
            last_category=Category.objects.get(name=category_path[-1])
            questions_file=Questions_file.objects.get(title=questions_file_title,category=last_category)
            return Question.objects.filter(questions_file=questions_file)
        except (Category.DoesNotExist,Questions_file.DoesNotExist):
            return Question.objects.none()

        

class AllChoiceOfAQuestionAPIView(generics.ListAPIView):
    serializer_class=ChoiceSerializer

    def get_queryset(self):
       category_path=self.kwargs.get('category_path','').split('/')
       questions_file_title=self.kwargs.get('questions_file','')
       question_id=self.kwargs.get('pk')

       try:
        last_category=Category.objects.get(name=category_path[-1])
        questions_file=Questions_file.objects.get(title=questions_file_title,category=last_category)
        question=Question.objects.get(id=question_id,questions_file=questions_file)
        return Choice.objects.filter(question=question)
       
       except (Category.DoesNotExist,Questions_file.DoesNotExist,Question.DoesNotExist):
        return Choice.objects.none()


class SubmitQuizAPIView(APIView):
    def post(self, request, category_path,questions_file):
        # Expecting {"choices": {question_id: choice_id, ...}, "is_submitted": true}
        choices = request.data.get("choices", {})
        is_submitted = request.data.get("is_submitted", True)

        if not choices:
            return Response({"error": "No choices provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Questions_file
        category_path_list=category_path.split('/')
        try:
            last_category=Category.objects.get(name=category_path_list[-1])
            

            questions_file_obj = get_object_or_404(
            Questions_file,
            title=questions_file,
            category=last_category
        )
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)    
            
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
        category_path=self.kwargs.get('category_path', '').split('/')
        questions_file_title=self.kwargs.get('questions_file')
        
        try:
            last_category=Category.objects.get(name=category_path[-1])
            questions_file=Questions_file.objects.get(title=questions_file_title,category=last_category)


            return get_object_or_404(
            UserQuizResult,
            user=self.request.user,
            questions_file=questions_file
            )
        
        except (Category.DoesNotExist,Questions_file.DoesNotExist):
            raise Http404("Quiz result not found ")
        




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


   